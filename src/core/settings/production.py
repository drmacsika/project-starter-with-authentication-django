import datetime
import os

from .base import *

DEBUG = False

SECRET_KEY = "Test"  # os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['.mydomain.com']

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email Settings
EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER ")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")  # SMTP_PASSWORD
ADMIN_EMAIL_MESSAGE_RECEIVER = os.environ.get("ADMIN_EMAIL_MESSAGE_RECEIVER")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL")

# Generic Settings for AWS
AWS_GROUP_NAME = os.environ.get("AWS_GROUP_NAME")
AWS_USERNAME = os.environ.get("AWS_USERNAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
expired_timeline = datetime.timedelta(days=3650)
date_expired_timeline_later = datetime.date.today() + expired_timeline
expires = date_expired_timeline_later.strftime("%A, %d %B %Y 20:00:00 GMT")
AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(expired_timeline.total_seconds()), ),
}

# AWS SES
# My Smtp Username that I got when create an SMTP user
AWS_SES_ACCESS_KEY_ID = os.environ.get("AWS_SES_ACCESS_KEY_ID")
# My Smtp Password that I got when create an SMTP user
AWS_SES_SECRET_ACCESS_KEY = os.environ.get("AWS_SES_SECRET_ACCESS_KEY")
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME")  # (ex: us-east-1)
AWS_SES_REGION_ENDPOINT = os.environ.get(
    "AWS_SES_REGION_ENDPOINT")  # (ex: email.us-east-2.amazonaws.com)

# Custom SES V4
IAM_USERNAME = os.environ.get("IAM_USERNAME")
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

# AWS S3
AWS_FILE_EXPIRE = 200
DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE")
STATICFILES_STORAGE = os.environ.get("STATICFILES_STORAGE")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
S3DIRECT_REGION = os.environ.get("S3DIRECT_REGION ")
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")
keypair_name_SSH_public_key = os.environ.get("keypair_name_SSH_public_key")

# AWS Cloudfront
CLOUD_FRONT_URL = os.environ.get("CLOUD_FRONT_URL")
MEDIA_URL = CLOUD_FRONT_URL + '/media/'
STATIC_URL = CLOUD_FRONT_URL + '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + '/admin/'
