#!/bin/bash
. $HOME/.bash_env
. /var/www/www.jesussaid.it/pyenv/bin/activate
exec python /var/www/www.jesussaid.it/app/manage.py $@
