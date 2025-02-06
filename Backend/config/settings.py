import os
from pathlib import Path
import environ

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False),
    GOOGLE_CLIENT_ID=(str, ''),
    GOOGLE_CLIENT_SECRET=(str, ''),
    GOOGLE_REDIRECT_URI=(str, 'http://localhost:8000/api/email/oauth2callback')
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file - add explicit error handling
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)
    print(f"Successfully loaded .env file from: {env_file}")
else:
    print(f"Warning: .env file not found at: {env_file}")

# Debug settings and environment variables
print(f"BASE_DIR: {BASE_DIR}")
print(f"GOOGLE_CLIENT_ID: {'Found' if env('GOOGLE_CLIENT_ID') else 'Not found'}")
print(f"GOOGLE_CLIENT_SECRET: {'Found' if env('GOOGLE_CLIENT_SECRET') else 'Not found'}")
print(f"GOOGLE_REDIRECT_URI: {env('GOOGLE_REDIRECT_URI')}")

# Google OAuth2 Settings
GOOGLE_CLIENT_ID = env('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = env('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = env('GOOGLE_REDIRECT_URI')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-default-secret-key')

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'apps.users',
    'apps.applications',
    'apps.reminders',
    'apps.ai_insights',
    'django_filters',
    'apps.teams',
    'apps.data_exchange',
    'apps.email_integration',
    'rest_framework_simplejwt',
]

# Custom user model
AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'job_tracker_db',
        'USER': 'bernardginnjr',
        'PASSWORD': 'GinnLand100201',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = 'Lax'  # Required for OAuth flow

# Optional: Additional CORS settings you might need
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

AUTHENTICATION_BACKENDS = [
    'apps.users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'users.User'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Create directories if they don't exist
MEDIA_DIRS = [
    os.path.join(BASE_DIR, 'media'),
    os.path.join(BASE_DIR, 'media', 'avatars'),
]

# Create directories if they don't exist
for dir_path in MEDIA_DIRS:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
DEFAULT_FROM_EMAIL = 'Job Tracker <no-reply@jobtracker.com>'

# OpenAI API Configuration
OPENAI_API_KEY = env('OPENAI_API_KEY', default='')

# Add this near the top of your settings.py
DEBUG = True  # Make sure this is True for development

# Add this for debugging
print(f"Django Debug: {DEBUG}")
print(f"Media URL: {MEDIA_URL}")
print(f"Media Root: {MEDIA_ROOT}")
print(f"Base Dir: {BASE_DIR}")

# Frontend URL for redirects
FRONTEND_URL = 'http://localhost:3000'  # Adjust this based on your frontend URL

# Update cache configuration for better OAuth state handling
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutes in seconds
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Email Integration Settings
EMAIL_INTEGRATION = {
    'CACHE_TIMEOUT': 3600,  # 1 hour for storing parsed emails
    'MAX_DAYS_BACK': 90,    # Maximum days to look back for emails
    'BATCH_SIZE': 50,       # Number of emails to process per batch
}

