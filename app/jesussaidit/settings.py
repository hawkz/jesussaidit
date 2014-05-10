"""
Django settings for jesussaidit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = '/var/www/www.jesussaid.it'


# Production / development switches
# https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['www.jesussaid.it']

SECRET_KEY = '40u=30%et#k$ehj4(f7eodv*h1rn3_qf0_4n5tm11@s1iihe9n'


# Email
# https://docs.djangoproject.com/en/1.6/ref/settings/#email

ADMINS = (
    ('Alex Tomkins', 'alex@blanc.ltd.uk'),
    ('Steve Hawkes', 'steve@blanc.ltd.uk'),
)

MANAGERS = ADMINS

SERVER_EMAIL = 'jesussaidit@blanctools.com'

DEFAULT_FROM_EMAIL = 'jesussaidit@blanctools.com'

EMAIL_SUBJECT_PREFIX = '[jesussaidit] '


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'jesussaidit.urls'

WSGI_APPLICATION = 'jesussaidit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jesussaidit_django',
        'USER': 'jesussaidit_django',
        'PASSWORD': 'AZWLAJ5XXwqA81Uk',
        'HOST': '2a01:7e00::2:9e09',
        'PORT': '5439',
    }
}


# Caches
# https://docs.djangoproject.com/en/1.6/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '[2a01:7e00::2:9ef1]:11211',
        'KEY_PREFIX': 'jesussaidit',
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '[2a01:7e00::2:9ef1]:11211',
        'KEY_PREFIX': 'jesussaidit',
        'TIMEOUT': 604800,  # 1 week
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/London'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs/static')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'app/static'),
)


# File uploads
# https://docs.djangoproject.com/en/1.6/ref/settings/#file-uploads

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'htdocs/media')


# Templates
# https://docs.djangoproject.com/en/1.6/ref/settings/#templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'app/jesussaidit/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)


# Logging
# https://docs.djangoproject.com/en/1.6/topics/logging/#configuring-logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}


# Any other application config goes below here

SITE_ID = 1


# Local settings override
try:
    from local_settings import *
except ImportError:
    pass
