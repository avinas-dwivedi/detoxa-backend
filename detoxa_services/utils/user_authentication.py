import jwt
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.conf import settings
from ..models.users import Users


class UserAuthentication(TokenAuthentication):

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            raise exceptions.AuthenticationFailed('Invalid Header')
        try:
            decoded_token = jwt.decode(authorization_header, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed("Invalid Token")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = Users.objects.filter(id=decoded_token.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        return user, None