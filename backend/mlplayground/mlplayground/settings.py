"""
Django settings for mlplayground project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import json
import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

# Discover which environment the server is running
ENV = os.getenv("DJANGO_ENV")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DJANGO_DEBUG", 0)))  # 0 is False

# A list of strings representing the host/domain names that this Django site can serve
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(" ")

# A list of trusted origins for unsafe requests (e.g. POST).
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(" ")

# Cors
CORS_ALLOW_ALL_ORIGINS = False  # If this is True then `CORS_ALLOWED_ORIGINS` will not have any effect

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = os.getenv("DJANGO_CORS_ALLOWED_ORIGINS", "").split(" ")

# Application definition
INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "drf_spectacular",
    "django_celery_results",
    "corsheaders",
    # Project apps
    "dqmio_file_indexer.apps.DqmioDataIndexerConfig",
    "dqmio_etl.apps.DqmioEtlConfig",
    "dqmio_celery_tasks.apps.DqmioCeleryTasksConfig",
    "custom_auth.apps.CustomAuthConfig",
]

# Django Rest Framework (DRF) configuration
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# DRF-Spectacular configuration
SPECTACULAR_SETTINGS = {"PREPROCESSING_HOOKS": ["mlplayground.spectacular.preprocessing_filter_spec"]}

# A list of middleware (framework of hooks into Django’s request/response processing) to use
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# A string representing the full Python import path to your root URLconf
ROOT_URLCONF = "mlplayground.urls"

# A list containing the settings for all template engines to be used with Django
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Indicate entrypoint for starting ASGI server
ASGI_APPLICATION = "mlplayground.asgi.application"


# Database configuration
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DJANGO_DATABASE_ENGINE"),
        "NAME": os.getenv("DJANGO_DATABASE_NAME"),
        "USER": os.getenv("DJANGO_DATABASE_USER"),
        "PASSWORD": os.getenv("DJANGO_DATABASE_PASSWORD"),
        "HOST": os.getenv("DJANGO_DATABASE_HOST"),
        "PORT": os.getenv("DJANGO_DATABASE_PORT"),
    },
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "WARNING",
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} - {asctime} - {module} - {message}",
            "style": "{",
        },
    },
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery configuration options
CELERY_BROKER_URL = os.getenv("DJANGO_CELERY_BROKER_URL")
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_CACHE_BACKEND = "django-cache"
CELERY_BEAT_SCHEDULE = {
    "Index new files and schedule ingestions": {
        "task": "dqmio_file_indexer.tasks.handle_periodic",
        "schedule": crontab(minute=0),
    }
}
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 60 * 60 * 24 * 2}  # seconds

# Path used in dqmio_file_indexer app to discover DQMIO files
DIR_PATH_DQMIO_STORAGE = os.getenv("DJANGO_DQMIO_STORAGE")

# Keycloak OIDC config
KEYCLOAK_SERVER_URL = os.getenv("DJANGO_KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM = os.getenv("DJANGO_KEYCLOAK_REALM")
KEYCLOAK_CONFIDENTIAL_CLIENT_ID = os.getenv("DJANGO_KEYCLOAK_CONFIDENTIAL_CLIENT_ID")
KEYCLOAK_CONFIDENTIAL_SECRET_KEY = os.getenv("DJANGO_KEYCLOAK_CONFIDENTIAL_SECRET_KEY")
KEYCLOAK_PUBLIC_CLIENT_ID = os.getenv("DJANGO_KEYCLOAK_PUBLIC_CLIENT_ID")
KEYCLOAK_API_CLIENTS = json.loads(os.getenv("DJANGO_KEYCLOAK_API_CLIENTS", "{}"))
