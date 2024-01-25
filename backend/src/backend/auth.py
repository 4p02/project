import jwt
import time
from constants import SECRET_KEY
from datetime import datetime, timedelta


def create_jwt_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload if payload['exp'] > time.time() else None
    except jwt.exceptions.DecodeError as e:
        print('Invalid token', "decode error", e)
        return None
