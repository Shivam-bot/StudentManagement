"""
Django settings for studentManagement project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, "studentManagement/.env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = json.loads(env('ALLOWED_HOST'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'studentDetails',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = json.loads(env("CORS_ALLOWED_ORIGINS"))

ROOT_URLCONF = 'studentManagement.urls'

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

WSGI_APPLICATION = 'studentManagement.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('ENGINE'),
        'NAME': env('NAME'),
        'USER': env('USER'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT': env('PORT')
    }
}

LOGGING = {
    'version': 1,  # Define version mandatory
    # Version of logging
    'disable_existing_loggers': False ,  # define whether to enable /disable django default logger
    # default true Formatters #######################################################
    'formatters': {

        # define the format of log as per req. Can be multiple
        #   To set format for  we have to add key formatt in handler and the specific format key

        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)s %(message)s'
        }
    },
    # disable logging
    # Handlers #############################################################
    'handlers': {
        # It'll generate the log. Level and encode define else default value should be taken.
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/loggerDjango-debug-io.log'),
            'formatter': 'verbose',  # Log format will be in the format define in verbose
            'encoding': 'utf-8',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/loggerDjango-info-io.log'),
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        ########################################################################
        'console': {
            'level': 'INFO',  # Set the level to INFO or DEBUG to capture info-level logs
            'class': 'logging.StreamHandler',
        },
    },
    # Loggers ####################################################################
    # Logger will transcribe every message
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],  # define the handles to be used while logging
            'propagate': True,  # To decide whether pass the message to ancestor log or not.
            # 'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
        'info_log': {
            'handlers': ['info'],
            'propagate': True,
            'level': os.getenv('INFO_LOG_LEVEL', 'INFO'),
        }

    },
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
