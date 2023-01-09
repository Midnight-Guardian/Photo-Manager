"""Django settings for testing Photo Manager project."""
from config.default_settings import * # noqa

ENVIRONMENT = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

AWS_ACCESS_KEY_ID = 'Test Access Key'
AWS_SECRET_ACCESS_KEY = 'Test Secret Key'
AWS_PHOTO_BUCKET_NAME = 'test_bucket'
