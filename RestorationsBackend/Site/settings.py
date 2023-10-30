from pathlib import Path
from configparser import ConfigParser
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG = ConfigParser()
CONFIG.read(BASE_DIR / 'config.cfg')
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
LOGS_DIR = BASE_DIR / 'logs'
INFO_LOG = LOGS_DIR / 'info.log'
ERR_LOG = LOGS_DIR / 'errors.log'

SECRET_KEY = CONFIG.get('Django', 'secret_key')
ALLOWED_HOSTS = ['127.0.0.1']
DEBUG = True

MONEY_SYMBOL = '₽'
DIGITS_RU_NAMES = {1_000_000_000: 'млрд.', 1_000_000: 'млн.', 1_000: 'тыс.'}

ROOT_URLCONF = 'Site.urls'
WSGI_APPLICATION = 'Site.wsgi.application'
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Restorations',
    'rest_framework',
    'drf_yasg',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':     CONFIG.get('Postgres DB', 'name'),
        'USER':     CONFIG.get('Postgres DB', 'user'),
        'PASSWORD': CONFIG.get('Postgres DB', 'password'),
        'HOST':     CONFIG.get('Postgres DB', 'host'),
        'PORT':     CONFIG.get('Postgres DB', 'port')
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.tokens.AccessToken',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_UPDATE_BLACKLIST_ON_LOGOUT': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'BLACKLISTED_TOKENS': {
        'access': 'rest_framework_simplejwt.token_blacklist.models.BlacklistedToken',
        'refresh': 'rest_framework_simplejwt.token_blacklist.models.BlacklistedToken',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INFO_LOG.touch(), ERR_LOG.touch()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'formatter': {
            'format': '{levelname} - {asctime} - {module} - {process:d} - {thread:d} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': INFO_LOG,
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': ERR_LOG,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['info', 'errors', 'console'],
            'formatter': 'formatter',
            'level': 'INFO',
            'propagate': False
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',          },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',         },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',        },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True