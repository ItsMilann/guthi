"""
Django settings example for the project
NOTE Use envrionment variables for sensitive variables such as secret, apikeys etc
"""

import os
from datetime import timedelta
from pathlib import Path
from corsheaders.defaults import default_headers

# pylint: disable=unnecessary-comprehension line-too-long

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY")

try:
    DEBUG = bool(int(os.environ.get("DEBUG", "1")))
except ValueError:
    DEBUG = True

ALLOWED_HOSTS = [host for host in os.environ.get("ALLOWED_HOSTS", "http://localhost").split(",")]

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    # cors config
    "corsheaders",
    # third party
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    # local
    "users.apps.UsersConfig",
    "templates.apps.TemplatesConfig",
    "branches.apps.BranchesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "project.urls"


WSGI_APPLICATION = "project.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# Cors Configs
WHITELIST = os.environ.get("WHITELIST", "http://localhost")

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [host for host in WHITELIST.split(",")]

CORS_ALLOW_HEADERS = list(default_headers) + ["apikey"]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework.authentication.TokenAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "EXCEPTION_HANDLER": "utilities.exceptions.custom_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "TIMEOUT": 60 * 60 * 30,
    }
}

AUTH_USER_MODEL = "users.User"
ACCESS_TOKEN_LIFETIME = os.environ.get("ACCESS_TOKEN_LIFETIME", 30)
REFRESH_TOKEN_LIFETIME = os.environ.get("REFRESH_TOKEN_LIFETIME", 30)
# JWT Token Configs
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=int(ACCESS_TOKEN_LIFETIME)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(REFRESH_TOKEN_LIFETIME)),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "user_email",
}

AUTH_SERVER_BASE_URL = os.environ.get("AUTH_SERVER_BASE_URL", "http://172.20.0.1:8848/")
AUTH_APP_ID = os.environ.get("AUTH_APP_ID", "9515647825802661")
AUTH_APP_SECRET = os.environ.get("AUTH_APP_SECRET", "ece5f64d7c5d438bbbdaf10e77abe506")


################### FEATURES ##############################
FEATURES = {
    # use auth service to authenticate user
    "USE_AUTH_SERVICE_TO_AUTHENTICATE": os.environ.get("USE_AUTH_SERVICE_TO_AUTHENTICATE"),
    # use auth service to login
    "ALLOW_OAUTH_LOGIN": os.environ.get("ALLOW_OAUTH_LOGIN"),
    # allow update requests on core apps such as nagarpalika, fiscal year
    "ALLOW_CORE_UPDATE": os.environ.get("ALLOW_CORE_UPDATE"),
    # sync updates from auth service
    "SYNC_WITH_AUTH_SERVICE": os.environ.get("SYNC_WITH_AUTH_SERVICE"),
    # send data to patrachar
    "FEATURE_DARTA": os.environ.get("FEATURE_DARTA"),
    "PROTECT_EMAIL": os.environ.get("PROTECT_EMAIL")
}
