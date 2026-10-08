from rest_framework import authentication
from rest_framework import exceptions
from .models import User
from .utils import decode_token

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        prefix = 'Bearer'
        if not auth_header.startswith(prefix):
            return None

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            raise exceptions.AuthenticationFailed('Invalid token format.')

        payload = decode_token(token)
        if not payload or payload.get('type') != 'access':
            raise exceptions.AuthenticationFailed('Invalid or expired token.')

        try:
            user = User.objects.get(id=payload['user_id'], is_active=True)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found or inactive.')

        return (user, token)
