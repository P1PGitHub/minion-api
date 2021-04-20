"""
Django settings for minionapi project.

Generated by 'django-admin startproject' using Django 2.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from corsheaders.defaults import default_headers
from datetime import timedelta
import os
import socket

import dj_database_url
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qba5%6mo#f6x!%$8kzy_cl8^b#u&$zxg83vkexrq)&lf9i)2f+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# DEBUG will add the devices current ip address to this list
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "minion-api.herokuapp.com",
    "minion-api-dev.herokuapp.com"
]

# Application definition
AUTH_USER_MODEL = "accounts.Account"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "reset_migrations",
    'corsheaders',
    'rest_framework',
    'accounts',
    'employee_logs',
    'reports',
    'teams',
    'projects',
    'notifications'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(
        'rest_framework.authentication.SessionAuthentication')

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://minion-spa.herokuapp.com",
    "https://minion-spa.herokuapp.com"
]


if DEBUG:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    ALLOWED_HOSTS.insert(0, ip_address)
    CORS_ALLOWED_ORIGINS.append(f"http://{ip_address}:3000")
    print(ALLOWED_HOSTS)
    print(ip_address)
    print(CORS_ALLOWED_ORIGINS)


CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'minionapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'minionapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # Development Database
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "d28kpnrun8naaa",
        'USER': "gtjekbkhxktfzu",
        'PASSWORD': "1bb5307cc29bf5be14590bcf43ee8083b9f96a1600e01a6cfa7e575686124d66",
        'HOST': "ec2-54-147-54-83.compute-1.amazonaws.com",
        'PORT': "5432",
    }
}

if not DEBUG:
    # Production Database
    db_from_env = dj_database_url.config(conn_max_age=600)
    DATABASES["default"].update(db_from_env)

firebase_cred = credentials.Certificate(
    os.path.join(BASE_DIR, "service_accounts/firebase.json"))
if DEBUG:
    firebase_admin.initialize_app(firebase_cred, {
        "storageBucket": "minion-upload-dev"
    })
else:
    firebase_admin.initialize_app(
        firebase_cred,
        {
            "storageBucket": "minion-upload.appspot.com"
        }
    )

BUCKET = storage.bucket()


EMAIL_HOST = "gator4212.hostgator.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "minion@priority1pos.com"
EMAIL_HOST_PASSWORD = "Minion#104"
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "minion@priority1pos.com"


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(os.path.normpath(BASE_DIR), "static")
]
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"
