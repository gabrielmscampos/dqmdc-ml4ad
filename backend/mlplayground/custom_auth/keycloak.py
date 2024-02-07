from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from utils.keycloak import Keycloak

kc = Keycloak(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CONFIDENTIAL_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_SECRET_KEY,
    realm_name=settings.KEYCLOAK_REALM
)


class KeycloakUser(AnonymousUser):
    """
    Django Rest Framework needs an user to consider authenticated
    """

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info

    @property
    def is_authenticated(self):
        return True


class KeycloakAuthentication(BaseAuthentication):
    """
    Custom authentication class based on Keycloak
    """

    def authenticate(self, request):
        token = self.__get_token(request)

        try:
            kc.validate_audience(token)
            kc.validate_authorized_party(token, settings.KEYCLOAK_PUBLIC_CLIENT_ID)
            kc.decode_token(token)
            user_info = kc.user_info(token)
        except Exception:
            raise AuthenticationFailed()

        return (KeycloakUser(user_info=user_info), None)

    @staticmethod
    def __get_token(request):
        token = request.headers.get("Authorization")
        if not token:
            raise AuthenticationFailed()
        try:
            return token.split("Bearer ")[-1]
        except AttributeError:
            raise AuthenticationFailed()


class KeycloakApiUser(AnonymousUser):
    """
    Django Rest Framework needs an user to consider authenticated
    """

    def __init__(self, token):
        super().__init__()
        self.token = token

    @property
    def is_authenticated(self):
        return True


class KeycloakApiTokenAuthentication(BaseAuthentication):
    """
    Custom authentication class based on Keycloak
    """

    def authenticate(self, request):
        api_key = self.__get_api_key(request)

        if api_key != settings.KEYCLOAK_SECRET_KEY:
            raise AuthenticationFailed()

        try:
            token = kc.issue_api_token()
        except Exception:
            raise AuthenticationFailed()

        return (KeycloakApiUser(token=token), None)

    @staticmethod
    def __get_api_key(request):
        token = request.headers.get("X-API-KEY")
        if not token:
            raise AuthenticationFailed()
        return token
