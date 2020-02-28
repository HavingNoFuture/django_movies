from .settings import *

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
]

INSTALLED_APPS += [
    'silk',
]
