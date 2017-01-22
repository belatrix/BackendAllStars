# settings/local.py
"""
If you use virtualenvwrapper add this line to ~/.virtualenvs/allstars/bin/postactivate
export DJANGO_SETTINGS_MODULE=AllStars.settings.local

"""

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Email
EMAIL_HOST = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST

# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# PUSH NOTIFICATIONS LOCAL
FIREBASE_SERVER_KEY = ''
