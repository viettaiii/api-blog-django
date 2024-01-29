from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .CustomTokenAuthentication import CustomTokenAuthentication


class AuthenticationPermissionMixin:
    authentication_classes = [SessionAuthentication, CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
