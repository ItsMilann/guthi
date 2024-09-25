"""
Import settings from settings.base module.
Overwrite settings, required for your environment.
For example in production, you might want to keep lifetime of access token very short.
"""
from .base import *  # pylint: disable=wildcard-import unused-wildcard-import

# https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/#conn-max-age
CONN_MAX_AGE = 60

# JWT Token Configs
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
}