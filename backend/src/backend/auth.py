from datetime import datetime, timedelta, timezone
from typing import TypedDict, Self, NamedTuple, Union, Optional

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError

from starlette.config import Config
from fastapi import Depends, Request
import bcrypt
from jwt import JWT
from jwt.jwk import OctetJWK
from jwt.exceptions import JWTDecodeError

from psycopg.rows import tuple_row

from backend import config, logger
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

    @property
    def role(self) -> str: return config.db.pgrest_auth_role

    def new(uid: int) -> Self:
        return Token(
            uid=uid,
            # account for clock drift on other clients, just in case
            nbf=(birth := datetime.now(timezone.utc) - timedelta(minutes=1)),
            exp=(birth + timedelta(days=config.auth.jwt_expiry_days)),
        )

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.exp
    def encode(self) -> str:
        data = self._asdict()
        data["nbf"] = int(data["nbf"].timestamp())
        data["exp"] = int(data["exp"].timestamp())
        data["role"] = self.role
        return JWT().encode(data, JWT_KEY, alg="HS512")

    def decode(token: str) -> Self:
        """May raise JWTDecodeError if expired or used before valid"""
        data = JWT().decode(token, JWT_KEY, algorithms=["HS512"])
        data = dict(
            (key, val) for (key, val) in data.items()
            if key in Token.__annotations__.keys()
        )
        try:
            data["nbf"] = datetime.fromtimestamp(data["nbf"], tz=timezone.utc)
            data["exp"] = datetime.fromtimestamp(data["exp"], tz=timezone.utc)
        except OverflowError as ex:
            raise JWTDecodeError("invalid timestamp") from ex

        return Token(**data)


def hash_password(password: str) -> str:
    """
    Hashes the given password with bcrypt.

    Note: this truncates the password to 72 chars; do not use longer passwords.
    """
    return bcrypt.hashpw(
        password=password.encode("utf-8"),
        salt=bcrypt.gensalt(rounds=config.auth.bcrypt_rounds)
    ).decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    """
    Determines if the password is equal to the bcrypt hash string.

    Note: this truncates the password to 72 chars; do not use longer passwords.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# todo: consider making a User model for these methods to return

async def login_user(db: Database, email: str, password: str) -> Optional[dict]:
    """May raise psycopg.Error on database error."""

    user = (await (await db.cursor().execute(
        """select id, email, fullname, password from private.users where email = %s""",
        (email, )
    )).fetchone())

    if user is None or not check_password(password, user["password"]):
        return None

    del user["password"]
    return user

async def get_document_by_url(db: Database, url: str) -> Optional[dict]:
    document = (await (await db.cursor().execute(
        """select * from public.documents where source_url = %s""",
        (url, )
    )).fetchone())
    
    return document

async def create_document(db: Database, source_url: str, body: bytes, summary: bytes, title: str, type: str = "webpage") -> Optional[dict]:
    
    document = (await (await db.cursor().execute(
        """
        insert into private.documents (type, source_url, body, summary, title) values (%s, %s, %s, %s, %s)
        returning id, created_at, type, source_url, body, summary, title;
        """,
        (type, source_url, body, summary, title)
    )).fetchone())
        
    return document

async def register_user(db: Database, email: str, password: str, fullname: str) -> Optional[dict]:
    async with db.transaction() as tx:  # fixme: this doesn't actually start a transaction!
        # don't register an email twice as it'll fail the uniqueness check
        cur = db.cursor()
        rows = (await cur.execute(
            """select email from private.users where email = %s""",
            (email, )
        )).rowcount

        if rows != 0: return None

        user = (await (await cur.execute(
            """
            insert into private.users (email, password, fullname) values (%s, %s, %s)
            returning id, created_at, email, fullname;
            """,
            (email, hash_password(password), fullname)
        )).fetchone())
        return user


async def get_link_from_id(db: Database, id: int) -> Optional[str]:
    link = (await (await db.cursor().execute(
        """select given_link from public.links where id = %s""",
        (id, )
    )).fetchone())
    return link


async def add_user_history(db: Database, document_id: int, link_id: int, user_id: int) -> Optional[dict]:
    history = (await (await db.cursor().execute(
        """
        insert into private.history (document_id, link_id, user_id) values (%s, %s, %s)
        returning id;
        """,
        (document_id, link_id, user_id)
    )).fetchone())
    return history

async def create_short_link(db: Database, given_link: str, uid: str) -> Optional[str]:
    if not uid:
        link = (await (await db.cursor().execute(
            """
            insert into public.links (given_link) values (%s)
            returning id;
            """,
            (given_link, )
        )).fetchone())
        return link
    
    link = (await (await db.cursor().execute(
        """
        insert into public.links (given_link, owner) values (%s, %s)
        returning id;
        """,
        (given_link, uid)
    )).fetchone())
    return link

async def check_if_user_exists(db: Database, email: str) -> bool:
    """May raise psycopg.Error on database error."""
    return (await (await db.cursor().execute(
        """select email, id from private.users where email = %s""",
        (email, )
    )).fetchone())

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
async def google_callback(db: Database, request:Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        e.add_note("Failed to authorize access token line 157 auth.py")
        raise e
    token_expiry = access_token['expires_at']
    user_info = access_token['userinfo']
    profile_picture = user_info['picture']
    given_name = user_info['given_name']
    family_name = user_info['family_name']
    email = user_info['email']
    print(token_expiry, profile_picture, given_name, family_name, email, "expire")
    user = await check_if_user_exists(db, email)
    if user is not None:
        return {"token": Token.new(user["id"]).encode()}
    # create the user
    user = await register_user(db, email, "password", given_name + " " + family_name)
    if user is not None:
        return {"token": Token.new(user["id"]).encode()}
    raise Exception("User not created line 175 auth.py")
