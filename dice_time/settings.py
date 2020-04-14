"""
Django settings for dice_time project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import logging
import os
import dotenv
import requests

dotenv.read_dotenv('dice.env')

RELEASE_UTC_DATETIME = os.getenv('RELEASE_UTC_DATETIME', '2020-04-08 17:00')
LOCAL = bool(int(os.getenv('LOCAL', '0')))
ADMIN_TG_IDS = [69062067, 144406]
API_TOKEN = os.getenv('API_TOKEN', '')
TG_API_HASH = os.getenv('TG_API_HASH', '')
TG_API_ID = os.getenv('TG_API_ID', '')
ORIGIN = os.getenv('ORIGIN', 'https://tg-dice-bot.avallon.im/')
REAL_TXS = True
FIELD_ENCRYPTION_KEY = os.getenv('MNEMONIC_ENCRYPTION_KEY')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = LOCAL

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "dicetime.club",
]
if LOCAL:
    ngrok_tunnels = 'http://localhost:4040/api/tunnels'
    resp = requests.get(ngrok_tunnels)
    ngrok_url = resp.json()['tunnels'][0]['public_url']
    ORIGIN = ngrok_url + '/'
    # ALLOWED_HOSTS.append(ORIGIN[8:-1])

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django_extensions',
    'encrypted_model_fields',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dice_time.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dice_time.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DB_NAME = os.getenv('DB_NAME', 'dicetime_dev')
DB_USER = os.getenv('DB_USER', 'dicebot')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PASS = os.getenv('DB_PASS', None)
DATABASES = {
    'sqlite': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         'ATOMIC_REQUESTS': True,
     },
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': DB_NAME,
       'USER': DB_USER,
       'PASSWORD': DB_PASS,
       'HOST': DB_HOST,
       'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

SUPPORTED_LANGUAGES = ['ru', 'en']
DEFAULT_LANGUAGE = 'en'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static'
MEDIA_ROOT = os.path.join(BASE_DIR, 'pictures')
MEDIA_URL = '/pictures/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

NODE_API_URL = os.getenv('NODE_API_URL', 'http://api.minter.one')

DJANGO_LOG_LEVEL = 'DEBUG'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} ({module}.{filename}:{lineno} {thread}|{process:d}) {levelname} - {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console'],
        #     # 'level': 'DEBUG',
        # },
        'TeleBot': {
            'handlers': ['console'],
            # 'level': 'DEBUG',
            'level': 'INFO',
        },
        'Dice': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    },
}