"""
Django settings for config project.
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ===========================================================================
# SECURITY SETTINGS
# ===========================================================================

# SECURITY WARNING: Production mein SECRET_KEY environment variable se lein!
# Terminal mein: export SECRET_KEY='your-very-secret-key-here'
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-guid7z))8b$+c=yr75s1^au9q+9n3g@zwe*mh31iny@l4sb!+b'  # Sirf development ke liye!
)

# SECURITY WARNING: Production mein DEBUG=False rakhein!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    '.localhost',
    '127.0.0.1',
    '[::1]',
    '.vercel.app',
    'freelancer-project-tracker-ayljnyez0.vercel.app',
]

# Production mein HTTPS settings (DEBUG=False hone par active honge)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True


# ===========================================================================
# APPLICATION DEFINITION
# ===========================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom SaaS Apps
    'accounts',
    'projects',
]

# Authentication Redirects
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files ke liye (Vercel/production)
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
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',   # <-- Yeh missing tha!
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ===========================================================================
# DATABASE
# ===========================================================================
# NOTE: Vercel pe SQLite kaam NAHI karta (ephemeral filesystem).
# Production ke liye PostgreSQL use karein (Supabase/Neon free hai).
#
# PostgreSQL ke liye:
#   pip install psycopg2-binary dj-database-url
#   Environment variable set karein: DATABASE_URL=postgresql://...
#
# Fir neeche wala code uncomment karein:
#
# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.config(
#         default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
#         conn_max_age=600,
#     )
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===========================================================================
# PASSWORD VALIDATION
# ===========================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===========================================================================
# INTERNATIONALIZATION
# ===========================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True


# ===========================================================================
# STATIC & MEDIA FILES
# ===========================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise: Production mein static files efficiently serve karta hai
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ===========================================================================
# BOOTSTRAP 5 MESSAGE TAGS
# ===========================================================================

MESSAGE_TAGS = {
    messages.DEBUG:   'alert-secondary',
    messages.INFO:    'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR:   'alert-danger',
}

# ===========================================================================
# DEFAULT SETTINGS
# ===========================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'