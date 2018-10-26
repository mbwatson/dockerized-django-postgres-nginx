from .settings import *

# Define production-specific Django settings here
#################################################

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-l+gzr40i$^m=4r%$ab-j%*$!z09oc7+ra7o_q!^^qeu22-td2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# DEBUG_PROPAGATE_EXCEPTIONS = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
        'NAME': os.environ.get('POSTGRES_DB', 'postgres_db'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres_password'),
    }
}
