# settings/local.py
"""
If you use Heroku type this command line:
heroku config:set DJANGO_SETTINGS_MODULE=AllStars.settings.production
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'