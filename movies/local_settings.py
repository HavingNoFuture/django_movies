from .settings import *
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'shx%(smjq5p&%nc&9ub^!3dil0zpbl!u*qcityb)b%1#f^#!7-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


RECAPTCHA_PUBLIC_KEY = '6LfK598UAAAAAL_L6r3rGEU17QjutgbtezxwRu_S'
RECAPTCHA_PRIVATE_KEY = '6LfK598UAAAAAClH5fCrpProLgpWTLADVy1Mn_0u'


EMAIL_HOST_USER = 'mail@gmail.com'
EMAIL_HOST_PASSWORD = 'password'


#  Тестирования запросов. Только в DEBUG.
MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
]

INSTALLED_APPS += [
    'silk',
]
