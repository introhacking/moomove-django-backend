from pathlib import Path
from datetime import timedelta
import os

from dotenv import load_dotenv,dotenv_values

config={
    **dotenv_values('constant_env/.env.shared'),
    **dotenv_values('constant_env/.env.secret'),
    # **os.environ
}

# Base settings
BASE_DIR = Path(__file__).resolve().parent.parent
# SECRET_KEY = 'django-insecure-*xn$u(lg+-z1u_uld9chorb)qgy3^vp-quu38e0*&%ff(83hie'
SECRET_KEY= f'{config["SECRET_KEY"]}'
DEBUG = True
ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = 'uauth.User'

# Installed apps
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
    'uauth',

    # New for Google Login
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

# Middleware
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'allauth.account.middleware.AccountMiddleware',
#     'uauth.middleware.AuditMiddleware',  # Custom middleware
# ]

MIDDLEWARE = [
    # Security and session-related middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # CORS middleware should come early to handle cross-origin requests
    'corsheaders.middleware.CorsMiddleware',
    
    # Middleware for common tasks and CSRF protection
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Authentication and user-related middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Middleware for clickjacking protection
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Third-party middleware for Allauth (Google login)
    'allauth.account.middleware.AccountMiddleware',
    
    # Custom middleware, placed after authentication to ensure user context is available
    'uauth.middleware.AuditMiddleware',
    
]


# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

CORS_ALLOWED_ORIGINS = [
    f'http://{config["FRONTEND_HOST"]}:4200',  # Adjust to match your frontend URL
    
    # Add other allowed origins as needed
    f'{config["HOST_URL"]}',    # TEST FOR AWS 
    f'http://{config["HOST_IP"]}'    # TEST
    
] 

# Simple JWT configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Add the path to your templates directory
        'APP_DIRS': True,  # Automatically look for templates in the app's 'templates' folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required for the admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
ROOT_URLCONF = 'shipment.urls'
# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',  # For Google login
)

# Google OAuth settings
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': ['profile', 'email'],
#         'AUTH_PARAMS': {'access_type': 'offline'},
#     }
# }

# Google credentials
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#          'SCOPE': ['profile', 'email'],
#         'AUTH_PARAMS': {'access_type': 'online'},
        
#         'APP': {
#             'client_id': f'{config["GOOGLE_CLIENT_ID"]}',
            
#             'secret': f'{config["GOOGLE_SECRET_KEY"]}',
            
#             'key': ''
#  }
#  }
# }

# LOGIN_REDIRECT_URL = f'{config["LOGIN_REDIRECT_URL"]}'
# redirect_uri = f'{config["GOOGLE_REDIRECT_URI"]}'
# LOGOUT_REDIRECT_URL = f'{config["LOGOUT_REDIRECT_URL"]}'


# DATABASE CONNECTION HERE
DATABASES = {
    'default': {
        'ENGINE': config['ENGINE'],
        'NAME': config['DATABASE_NAME'],
        'USER': config['DATABASE_USERNAME'],
        'PASSWORD': config['DATABASE_PASSWORD'],
        'HOST': config['HOST'],
    }
}

# Static and media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Additional configurations
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
