import time
from datetime import datetime, timedelta
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError

from fastapi import Depends, Request
import jwt
import time

from backend import config
from datetime import datetime, timedelta
from starlette.config import Config

from db import Database
database = Database()



# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': config.google_client_id, 'GOOGLE_CLIENT_SECRET': config.google_client_secret}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


def create_jwt_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=config.jwt_expiry_days),
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



#when register is called, the email, name and password are stored into a database taboe

def register(email: str, password: str, full_name: str) -> bool:
    try:
        # Call the register method from Routes
        database.register_user(full_name, email, password)
        return {"data": "true"}  # Return the result from the register method
    except Exception as e:
        # Handle any exceptions that occur during registration
        print("Error occurred during registration:", e)
        return False

    """_summary_
    login function, will check if the email and password pair exists in the db
    """
def login(email: str, password: str) -> bool:
    if(database.login_user(email, password)):
        return {"login": "true"}
    else:
        return {"login": "false"}


async def google(request: Request):
    return await oauth.google.authorize_redirect(request, config.google_callback_uri)


"""

TODO
    validate email in database and generate JWT token
    return the JWT token to the user
Handle google oauth callback
@param request: Request
@return: dict with jwt token
"""
async def google_callback(request:Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise "Oauth in da house"
    token_expiry = access_token['expires_at']
    user_stuff = access_token['userinfo']
    profile_picture = user_stuff['picture']
    given_name = user_stuff['given_name']
    family_name = user_stuff['family_name']
    email = user_stuff['email']
    print(token_expiry, profile_picture, given_name, family_name, email, "expire")
    token_jwt = "123"
    return {'result': True, 'access_token': token_jwt}


