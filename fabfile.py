# -*- coding: utf-8 -*-

import random

from fabric.api import cd, env, execute, local, parallel, roles, run, runs_once, task
from fabric.contrib.files import exists

# Changable settings
env.roledefs = {
    'web': [
        'jesussaidit@scorch.devsoc.org',
        'jesussaidit@smaug.devsoc.org',
    ],
    'cron': [
        'jesussaidit@smaug.devsoc.org',
    ],
}

env.home = env.get('home', '/var/www/jesussaidit')
env.repo = env.get('repo', 'jesussaidit')
env.media = env.get('media', 'jesussaidit')
env.database = env.get('database', 'jesussaidit_django')

CRONTAB = """
MAILTO=""

{daily}         /usr/local/bin/django-cron python manage.py clearsessions
"""

# Avoid tweaking these
env.use_ssh_config = True
GIT_REMOTE = 'git@github.com:developersociety/{env.repo}.git'
DATABASE_SERVER = 'golestandt.devsoc.org'


@task
@roles('cron')
def cron(remove=None):
    """
    Crontab setup.

    Can also be removed if needed.

    fab cron
    fab cron:remove=True
    """
    # Allow quick removal if needed
    if remove:
        run('crontab -r')
        return

    # Deterministic based on hostname
    random.seed(env.host_string)

    # Several templates - can add more if needed
    def every_x(minutes=60, hour='*', day='*', month='*', day_of_week='*'):
        # Add some randomness to minutes
        start = random.randint(0, minutes - 1)
        minute = ','.join(str(x) for x in range(start, 60, minutes))

        return '{minute} {hour} {day} {month} {day_of_week}'.format(
            minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week)

    daily = every_x(hour=random.randint(0, 23))
    hourly = every_x()

    cron = CRONTAB.format(daily=daily, hourly=hourly)

    run("echo '{}' | crontab -".format(cron))


@task
@roles('web')
@parallel
def clone_repo(branch='master'):
    """
    Initial site setup.

    Only intended to be run once, but can be used to switch branch.

    fab clone_repo
    fab clone_repo:branchname
    """
    with cd(env.home):
        if not exists('.git'):
            git_repo = GIT_REMOTE.format(env=env)
            run('git clone --quiet --recursive {} .'.format(git_repo))
        else:
            run('git fetch')

        run('git checkout {}'.format(branch))


@task
@roles('web')
@parallel
def update():
    """ Pull latest git repository changes and install requirements. """
    with cd(env.home):
        run('git pull')

        run('pip install --quiet --requirement requirements.txt')

        # Clean up any potential cruft
        run('find . -name "*.pyc" -delete')


@task
@runs_once
@roles('web')
def migrate():
    """ Migrate database changes. """
    with cd(env.home):
        run('python manage.py syncdb')


@task
@roles('web')
@parallel
def static():
    """ Update static files. """
    with cd(env.home):
        # Collect static files
        run('python manage.py collectstatic --verbosity=0 --noinput')


@task(name='reload')
@roles('web')
@parallel
def reload_uwsgi(force_reload=None):
    """
    Reload uWSGI.

    fab reload
    fab reload:True
    fab reload:force_reload=True
    """
    if force_reload:
        run('killall -TERM uwsgi')
    else:
        run('killall -HUP uwsgi')


@task
@roles('web')
@runs_once
def sentry_release():
    """ Register new release with Sentry. """
    with cd(env.home):
        version = run('sentry-cli releases propose-version')
        run('sentry-cli releases new --project {project} {version}'.format(
            project=env.repo, version=version
        ))
        run('sentry-cli releases set-commits --auto {version}'.format(version=version))


@task
def deploy(force_reload=None):
    """
    Deploy to remote server.

    Steps includes pull repo, migrate, collect static, install requirements.

    fab deploy
    fab deploy:True
    fab deploy:force_reload=True
    """
    execute(update)
    execute(migrate)
    execute(static)
    execute(reload_uwsgi, force_reload=force_reload)
    execute(cron)
    execute(sentry_release)


@task
def get_backup(hostname=None, replace_hostname='127.0.0.1', replace_port=8000):
    """
    Get remote backup and restore database locally.

    fab get_backup
    fab get_backup:www.example.com
    fab get_backup:www.example.com,192.1.1.1
    fab get_backup:hostname=www.example.com,replace_hostname=192.1.1.1,replace_port=8000
    """
    # Recreate database
    local('dropdb --if-exists {}'.format(env.database))
    local('createdb {}'.format(env.database))

    # Connect to the server and dump database.
    commands = ['ssh -C {} sudo -u postgres pg_dump --no-owner {}'.format(
        DATABASE_SERVER, env.database
    )]

    if hostname:
        # If hostname is passed replace with replace_hostname.
        commands.append('sed -e "s|{}|{}:{}|g"'.format(
            hostname, replace_hostname, replace_port
        ))

    # Restore database.
    commands.append('psql --single-transaction {}'.format(env.database))

    local(' | '.join(commands))
