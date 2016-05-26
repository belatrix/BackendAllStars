# settings/local.py
"""
If you use Heroku type this command line:
heroku config:set DJANGO_SETTINGS_MODULE=AllStars.settings.production
"""
import dj_database_url
from .base import *
from os import environ


# Function to get environment variables value if they exist.
def env(e, d):
    if e in environ:
        return environ[e]
    else:
        return d

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Apps
PRODUCTION_APPS = [
    'storages',
]

INSTALLED_APPS += PRODUCTION_APPS

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Email
EMAIL_HOST = env('EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', '')
EMAIL_PORT = env('EMAIL_PORT', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST

# AWS
AWS_STORAGE_BUCKET_NAME = 'allstarsbx'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '')
AWS_QUERYSTRING_AUTH = False

# MEDIA
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = 'https://allstarsbx.s3.amazonaws.com/media/'
DEFAULT_FILE_STORAGE = 'utils.custom_storages.MediaStorage'
