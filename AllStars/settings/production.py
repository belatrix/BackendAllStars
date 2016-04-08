# settings/local.py
"""
If you use Heroku type this command line:
heroku config:set DJANGO_SETTINGS_MODULE=AllStars.settings.production
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
