import jwt
import datetime
from .config import Config


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return str(e)

