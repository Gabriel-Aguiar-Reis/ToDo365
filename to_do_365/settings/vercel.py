from to_do_365.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['.vercel.app']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'todo365',
        'USER': 'adminposte',
        'PASSWORD': 'hXkfuuJLwuuloHuMWxyDaLnSfEuZNqz0',
        'HOST': 'dpg-cl9amfto7jlc73b0c78g-a',
        'PORT': '5432',
    }
}