from datetime import datetime, timedelta, timezone
from typing import TypedDict, Self, NamedTuple, Union

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError

from starlette.config import Config
from fastapi import Depends, Request
import bcrypt
from jwt import JWT
from jwt.jwk import OctetJWK
from jwt.exceptions import JWTDecodeError

from backend import config
from backend.db import Database



# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': config.auth.google_client_id, 'GOOGLE_CLIENT_SECRET': config.auth.google_client_secret}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

JWT_KEY = OctetJWK(config.auth.jwt_secret.encode("utf-8"))

class Token(NamedTuple):
    uid: int
    nbf: datetime
    exp: datetime

    def new(uid: int) -> Self:
        return Token(
            uid=uid,
            # account for clock drift on other clients, just in case
            nbf=(birth := datetime.now(timezone.utc) - timedelta(minutes=1)),
            exp=(birth + timedelta(days=config.auth.jwt_expiry_days)),
        )

    def encode(self) -> str:
        data = self._asdict()
        data["nbf"] = int(data["nbf"].timestamp())
        data["exp"] = int(data["exp"].timestamp())
        return JWT().encode(data, JWT_KEY, alg="HS512")

    def decode(token: str) -> Self:
        """May raise JWTDecodeError if expired or used before valid"""
        data = JWT().decode(token, JWT_KEY, algorithms=["HS512"])
        try:
            data["nbf"] = datetime.fromtimestamp(data["nbf"], tz=timezone.utc)
            data["exp"] = datetime.fromtimestamp(data["exp"], tz=timezone.utc)
        except OverflowError as ex:
            raise JWTDecodeError("invalid timestamp") from ex

        return Token(**data)


def api_key_auth(api_key):
    # decoded_token = decode_jwt_token(api_key)
    # if decoded_token is None:
    #     return False
    return True


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password

def dehash_password(password: str, hashed_password: str) -> str:
    return bcrypt.checkpw(password, hashed_password)

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
    user_info = access_token['userinfo']
    profile_picture = user_info['picture']
    given_name = user_info['given_name']
    family_name = user_info['family_name']
    email = user_info['email']
    print(token_expiry, profile_picture, given_name, family_name, email, "expire")
    token_jwt = "123"
    return {'result': True, 'access_token': token_jwt}


