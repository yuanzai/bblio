"""
Django settings for Build0001 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import sys
sys.path.append('/home/ec2-user/bblio')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kh(odjhmig8dvjgv%vvrt4*s$zn91lo!2waa0hqact7n5x-nw+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'search',
    'operations',
    'testscrape',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Build.urls'

WSGI_APPLICATION = 'Build.wsgi.application'

# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scrapedata',
	'USER': 'root',
	'PASSWORD': '',
	'HOST': '127.0.0.1',
	'PORT': '3306',
    },
    
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scrapedata',
        'USER': 'yuanzai',
        'PASSWORD': 'wakaff01',
        'HOST': 'bblio.cxo6rxxzg0qa.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#STATIC_ROOT = '/home/ec2-user/bblio/build/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
        )
