from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

from django.urls import reverse_lazy


# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7ist2%6a!h%0pio9+cxl-7n_+qwerty4+##ojsts(4!g3y**exj9klxv'

# SECURITY WARNING: don't run with debug turned on in production!
# TODO move to env
DEBUG = False

ALLOWED_HOSTS = ['*']

# ログイン・ログアウト後の遷移を規定
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')

HTTP_SCHEMA = 'http'
DOMAIN = 'localhost:8000'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'debug_toolbar',
    'rangefilter',
    'import_export',
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'rest_framework_simplejwt',
    'storages',

    'currency',  # それぞれのмодульのurls集を独自に作ること。後の混乱を防ぐ。
    'accounts',
    # 'silk',
    'crispy_forms',
]

MIDDLEWARE = [
    # 'silk.middleware.SilkyMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'currency.middlewares.ResponseTimeMiddleware',  # 登録して動かすための一行
    # 'currency.middlewares.GclidMiddleware',
]

ROOT_URLCONF = 'settings.urls'

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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'currency',
        'USER': 'db-user',
        'PASSWORD': 'postgres-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'  # これによりDjangoは、auth_userではなくこのuserで操作できる

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = BASE_DIR / '..' / 'static_content' / 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / '..' / 'static_content' / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',
    '172.31.69.226',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # どのようにemailを送るか
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # shellコンソールで表示、実際には送られない
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'python.test.yoshio@gmail.com'  # от кого
EMAIL_HOST_PASSWORD = 'pythontest001'
SUPPORT_EMAIL = 'python.test.yoshio@gmail.com'  # получатель この場合サポートセンター

CELERY_BROKER_URL = 'amqp://localhost'  # Broker(Rabbitmq)のアドレス。ここにProducer(Django)とConsumer(Celery)がアクセスする

# 定期的なタスク
CELERY_BEAT_SCHEDULE = {
    'alfabank': {
        'task': 'currency.tasks.parse_alfabank',
        'schedule': crontab(minute='*/15'),
    },
    'monobank': {
        'task': 'currency.tasks.parse_monobank',
        'schedule': crontab(minute='*/15'),
    },
    'ukrgasbank': {
        'task': 'currency.tasks.parse_ukrgasbank',
        'schedule': crontab(minute='*/15'),
    },
    'otpbank': {
        'task': 'currency.tasks.parse_otpbank',
        'schedule': crontab(minute='*/15'),
    },
    'privatbank': {
        'task': 'currency.tasks.parse_privatbank',
        'schedule': crontab(minute='*/15'),
    },
    'vkurse_dp_ua': {
        'task': 'currency.tasks.parse_vkurse_dp_ua',
        'schedule': crontab(minute='*/15'),
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # コメント化するとキャッシュを止められる

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),  # 401（←誰か分かりませんでした） どのようにユーザーのステータスの見分けるか
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),  # 403（←誰か分かるけど権限なかったよ） ユーザーのアクセス権限を見分ける。全体にアクセス制限する。もしくはviewsでviewごとに制限かけることもできる。
    'DEFAULT_THROTTLE_RATES': {
        'rates_anon_throttle': '20/min',
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer', 'JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# AWS_S3_REGION_NAME = 'fra1'
# AWS_S3_ENDPOINT_URL =
# AWS_ACCESS_KEY_ID =
# AWS_SECRET_ACCESS_KEY =
# STATICFILES_STORAGE =
# AWS_STORAGE_BUCKET_NAME =
# STATIC_URL =
# AWS_DEFAULT_ACL = 'public-read'
