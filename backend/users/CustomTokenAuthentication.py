from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import User
import jwt

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token', None)
        if not token:
            raise exceptions.AuthenticationFailed("Token is not existing!")
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token is invalid")

        user = User.objects.filter(id=payload['id']).first()
        if user:
            return (user, None)
        return None
