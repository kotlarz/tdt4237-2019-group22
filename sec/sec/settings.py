"""
Django settings for sec project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import logging
import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# FIXME: Replace in production
SECRET_KEY = '$n%^#g%qx#82w6t^dvjqwv)q*1cy+fwh1ohku7-rbjqcei2^jr'


DEBUG = False

#TODO
""""Set path and domain"""
#SESSION_COOKIE_PATH='';
#SESSION_COOKIE_DOMAIN='';


ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sec',
    'projects.apps.ProjectConfig',
    'home.apps.HomeConfig',
    'user.apps.UserConfig',
    'bootstrap4',
    'django_icons',
    'payment.apps.PaymentConfig',
]

# FIXME: Security Misconfiguration - Remove, server2 header, etc. in production (InformationMiddleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'sec.middleware.SimpleSessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'sec.middleware.InformationMiddleware',
]

X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'sec.urls'

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

WSGI_APPLICATION = 'sec.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher'
]

# Login redirect
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# FIXME: Broken Access Control - Private media storage
# TODO: Lookup django-private-storage or django-filer
"""
Users may open uploaded project files that they do not have permissions for, by
entering the URL directly.
"""
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# FIXME: MIME-Type sniffing vulnerability:
# TODO: https://docs.djangoproject.com/en/dev/ref/settings/#secure-content-type-nosniff
"""
It is possible for an attacker to leverage MIME sniffing to determine a different file type
and cause the execution of malicious script. For example, malicious file can be “translated”
by the browser as an image jpg. Thus, browser will execute it as an HTML and therefore
causing the execution of malicious script.
"""


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local_settings import *
except ModuleNotFoundError:
    logging.getLogger(__name__).critical("Local settings are not defined")
