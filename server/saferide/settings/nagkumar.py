from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'saferide',
        'USER': 'nagkumar',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MAILGUN_SECRET_KEY = 'key-d14e446a351d68d5ed2073b1e10f3fc4'
MAILGUN_PUBLIC_KEY = 'pubkey-97e7bda2036d652a299215df78805fb9'
MAILGUN_API_URL = "https://api.mailgun.net/v3/mailgun.nagkumar.com/messages"

DEFAULT_TOKEN = 'f42ca8b084bd199f0c4a726e77a9b84f899bf094'
