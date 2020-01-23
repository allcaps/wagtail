import socket

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$fz_eoy_i-ie6uiejz5%&@p9q5-f6^4#ni4lra+uu3xtatwm!-'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SELENIUM_HEADLESS = True
SELENIUM_REMOTE_URL = "http://localhost:4444/wd/hub"

# SESSION_COOKIE_DOMAIN = "192.168.2.1"

try:
    from .local import *
except ImportError:
    pass
