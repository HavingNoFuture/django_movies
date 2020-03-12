from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'shx%(smjq5p&%nc&9ub^!3dil0zpbl!u*qcityb)b%1#f^#!7-'


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
