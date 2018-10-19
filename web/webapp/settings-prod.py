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

