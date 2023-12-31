import dj_database_url

from to_do_365.settings.base import *

DEBUG = 'RENDER' not in os.environ
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://todo365databaseuser:ie02qmCYPEunZrsSUrYsqO2mQmT7rpFT@dpg-cljbfq700qrs73e089pg-a/todo365database',
    )
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'Todo365',
#         'USER': 'adminposte',
#         'PASSWORD': 'hXkfuuJLwuuloHuMWxyDaLnSfEuZNqz0',
#         'HOST': 'dpg-cl9amfto7jlc73b0c78g-a',
#         'PORT': '5432',
#     }
# }

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
