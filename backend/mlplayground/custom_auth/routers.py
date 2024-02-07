from rest_framework import routers

from .viewsets import KeycloakExchangeViewSet

router = routers.SimpleRouter()
router.register(r"exchange-token", KeycloakExchangeViewSet, basename="exchange-token")
