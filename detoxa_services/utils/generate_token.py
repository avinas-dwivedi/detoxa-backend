import datetime
import jwt
from detoxa_backend import settings


def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.JWT_SECRET_KEY, algorithm='HS256')
    return access_token