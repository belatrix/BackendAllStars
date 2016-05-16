"""
Django settings for AllStars project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6!)5-*-&azs8)4jdepx@gmcqhh65e*w93u18s3g^hw9fhq&b(p'

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'djoser',
    'corsheaders',
    'import_export',
    'categories',
    'employees',
    'events',
    'stars',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AllStars.urls'

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ('GET',
                      'POST',
                      'PUT',
                      'PATCH',
                      'DELETE',
                      'OPTIONS')
CORS_ALLOW_HEADERS = ('x-requested-with',
                      'content-type',
                      'accept',
                      'origin',
                      'authorization')
CORS_EXPOSE_HEADERS = ('Access-Control-Allow-Origin',
                       'Access-Control-Allow-Headers')

# REST
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# USER MODEL
AUTH_USER_MODEL = "employees.Employee"
NEXT_LEVEL_SCORE = 25

# DJOSER
DJOSER = {
    'DOMAIN': 'belatrixsf.com',
    'SITE_NAME': 'Belatrix All Stars',
    'SET_PASSWORD_RETYPE': False,
}

# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_DOMAIN = 'belatrixsf.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMPLOYEE CREATION MESSAGES
EMPLOYEE_CREATION_SUBJECT = '[BELATRIX AllStars] Your account was created successfully.'
EMPLOYEE_RESET_PASSWORD_CONFIRMATION_SUBJECT = '[BELATRIX AllStars] Please confirm if you want a password reset.'
EMPLOYEE_RESET_PASSWORD_SUCCESSFUL_SUBJECT = '[BELATRIX AllStars] Your new password has been successfully created.'

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

WSGI_APPLICATION = 'AllStars.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {}
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__ + '/../../'))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
