import time
from constants import SECRET_KEY, NUMBER_OF_DAYS_TO_EXPIRE
from datetime import datetime, timedelta

from fastapi import Depends
import jwt

from backend import config


def create_jwt_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=NUMBER_OF_DAYS_TO_EXPIRE),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, config.jwt_secret, algorithm='HS256')


def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, config.jwt_secret, algorithms=['HS256'])
        return payload if payload['exp'] > time.time() else None
    except jwt.exceptions.DecodeError as e:
        print('Invalid token', "decode error", e)
        return None


def api_key_auth(api_key):
    # decoded_token = decode_jwt_token(api_key)
    # if decoded_token is None:
    #     return False
    return True


def register(email: str, password: str, full_name: str) -> bool:
    return {"data": "true"} 


def login(email: str, password: str) -> bool:
    return {"data": "true"}



def google():
    return f'<h1>Google Page</h1>'

def google_callback():
    return f'<h1>Google Callback Page</h1>'
