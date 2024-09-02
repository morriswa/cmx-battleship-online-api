"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

# Hello World!

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Step 1)
# required deps
import os

from pathlib import Path
from dotenv import load_dotenv

# Step 2)
# set default properties
load_dotenv('default.properties')
# and load secrets to ENV
load_dotenv('secrets.properties')

# Step 3)
# setup django for rest application
INSTALLED_APPS = [
    # django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'corsheaders',
    # api modules
    'core',
    'user_session',
    'lobby',
    'game',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

WSGI_APPLICATION = 'app.wsgi.application'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Step 4)
# Init data sources
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Step 5)
# Env specific settings
RUNTIME_ENVIRONMENT = os.getenv('RUNTIME_ENVIRONMENT') or "prod"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if RUNTIME_ENVIRONMENT == "prod" else True

# Step 5.1)
# Security Setup
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# Include below to enable authentication and permission checks on every endpoint
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
#     'DEFAULT_AUTHENTICATION_CLASSES': ('app.authentication.PlayerAuthentication',),
# }
CORS_EXPOSE_HEADERS = ["session-id", "content-type", "content-length"]
CORS_ALLOW_HEADERS = CORS_EXPOSE_HEADERS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:4200',
    'https://www.morriswa.org',
]
ALLOWED_HOSTS = ['*']
CORS_ALLOW_METHODS = (
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
)
