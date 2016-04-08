# settings/local.py
"""
If you use virtualenvwrapper add this line to ~/.virtualenvs/allstars/bin/postactivate
export DJANGO_SETTINGS_MODULE=AllStars.settings.local

"""

from .base import *

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
