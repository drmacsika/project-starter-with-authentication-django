import os

from .base import *

DEBUG = False
print("Here in Prod")
SECRET_KEY = "Test"  # os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['.mydomain.com']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
