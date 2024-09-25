from __future__ import annotations
import typing
import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

if typing.TYPE_CHECKING:
    from users.models import User


def get_or_create_user(data, **kwargs) -> tuple[User, dict]:
    # pylint: disable=import-outside-toplevel
    """Update or create new user based on data."""
    from users.api.serializers import UserSerializer
    from users.models import User

    data = data.get("data", data)
    email = data["email"]

    qs = User.objects.filter(email=email)
    if qs.exists():
        instance = qs.latest("id")
        serializer = UserSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
    else:
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(**kwargs)
    instance.password = data["password"]
    instance.save()
    return instance, serializer.data


def exchange_auth_token(token) -> dict:
    BASE_URL = settings.AUTH_SERVER_BASE_URL
    ID = settings.AUTH_APP_ID
    SECRET = settings.AUTH_APP_SECRET
    URI = f"/api/v1/o/open-id/?id={ID}&token={token}&secret={SECRET}"
    URL = BASE_URL + URI
    respose = requests.get(URL)
    if respose.ok:
        user, data = get_or_create_user(respose.json())
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token), **data}
        return data
    try:
        raise AuthenticationFailed(respose.json())
    except requests.exceptions.JSONDecodeError as e:
        raise AuthenticationFailed(_("Failed to authenticate, try again later.")) from e


def exchange_auth_token_for_profile(token) -> dict:
    BASE_URL = settings.AUTH_SERVER_BASE_URL
    ID = settings.AUTH_APP_ID
    SECRET = settings.AUTH_APP_SECRET
    URI = f"/api/v1/o/profile/?id={ID}&token={token}&secret={SECRET}"
    URL = BASE_URL + URI
    respose = requests.get(URL)
    if respose.ok:
        return respose.json()
    try:
        raise AuthenticationFailed(respose.json())
    except requests.exceptions.JSONDecodeError as e:
        raise AuthenticationFailed(_("Failed to authenticate, try again later.")) from e


def get_user_with_email_from_auth_service(email: str) -> dict:
    BASE_URL = settings.AUTH_SERVER_BASE_URL
    ID = settings.AUTH_APP_ID
    SECRET = settings.AUTH_APP_SECRET
    URI = f"/api/v1/o/user/?id={ID}&email={email}&secret={SECRET}"
    URL = BASE_URL + URI
    respose = requests.get(URL)

    if respose.ok:
        if not int(ID) in respose.json()["data"]["scope"]:
            message_np = "तपाईलाई यो एप चलाउन अनुमति दिईएको छैन | कृपया पालिकामा सम्पर्क गर्नु होला | धन्यवाद |"
            raise AuthenticationFailed(message_np)
        user, data = get_or_create_user(respose.json())
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token), **data}
        return data

    try:
        raise AuthenticationFailed(respose.json())
    except requests.exceptions.JSONDecodeError as e:
        raise AuthenticationFailed(_("Failed to authenticate, try again later.")) from e
