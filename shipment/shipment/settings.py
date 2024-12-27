"""
Django settings for shipment project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv,dotenv_values

config={
    **dotenv_values('constant_env/.env.shared'),
    **dotenv_values('constant_env/.env.secret'),
    # **os.environ
}

# Test retrieval with os.getenv
# print("HOST NAME : "+ config['HOST'])

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*xn$u(lg+-z1u_uld9chorb)qgy3^vp-quu38e0*&%ff(83hie'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL='uauth.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'drf_spectacular',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'aggregator',
    'rest_framework.authtoken',
    'uauth'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Downloaded Middleware
    'uauth.middleware.AuditMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
#    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#    'PAGE_SIZE': 10,    
}
CORS_ALLOWED_ORIGINS = [
    f'http://{config["FRONTEND_HOST"]}:4200',  # Adjust to match your frontend URL
    # Add other allowed origins as needed
    # 'http://35.154.191.16:8000', # PRODUCTION
    # 'http://moomove-ui-deploy.s3-website.ap-south-1.amazonaws.com/'    # PRODUCTION FOR AWS 

    f'http://{config["HOST"]}/'    # TEST FOR AWS 
    f'http://{config["HOST_IP"]}',    # TEST
    
] 

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Shipment API',
    'DESCRIPTION': 'API documentation for the Shipment project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
ROOT_URLCONF = 'shipment.urls'

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

WSGI_APPLICATION = 'shipment.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# LOCAL DATABASE CONNECTION HERE

DATABASES = {
    'default': {
        'ENGINE': config['ENGINE'],
        'NAME': config['DATABASE_NAME'],
        'USER': config['DATABASE_USERNAME'],
        'PASSWORD': config['DATABASE_PASSWORD'],
        'HOST': config['HOST'],
    }
}

# CLOUD(AWS) DATABASE CONNECTION HERE

# endpoint: moomovedb.cncigou2sueo.ap-south-1.rds.amazonaws.com
# pwd: Moomove123
# user: moomove

#  NEW DATABASE CONFIG DETAILS
# endpoint: moomovedb.cncigou2sueo.ap-south-1.rds.amazonaws.com
# pwd: pushparaj
# user: pushparaj

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'moomove_DB',
#         'USER': 'moomove',
#         'PASSWORD': 'Moomove123',
#         'HOST': 'moomovedb.cncigou2sueo.ap-south-1.rds.amazonaws.com',
#         'PORT': '5432'
#     }
# }

# TEST DATABASE CONFIG DETAILS

# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.postgresql',
#          'NAME': 'testdbbymanish',
#          'USER': 'testdbbymanish',
#          'PASSWORD': 'testdbbymanish',
#          'HOST': 'testdbbymanish.cncigou2sueo.ap-south-1.rds.amazonaws.com',
#          'PORT': '5432',
#      }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Define the directory where static files are collected
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Define the directory where media files (uploaded files) are stored
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         },
#     }
# }


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<Your-Client-ID>'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<Your-Client-Secret>'