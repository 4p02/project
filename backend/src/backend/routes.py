from typing import Optional, Tuple

from fastapi import APIRouter, Depends, Request, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser,
    requires
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection

from jwt.exceptions import JWTDecodeError

from backend import config
from backend.auth import api_key_auth, google, google_callback, login, register, Token
from backend.db import Database
from backend.models import Login, Register, Summarize
from backend.misc import handle_and_log_exceptions


class JWTUser(BaseUser):
    token: Token
    def __init__(self, token: Token) -> None: self.token = token

    @property
    def is_authenticated(self) -> bool: return True


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Optional[Tuple[AuthCredentials, BaseUser]]:
        if "Authorization" not in conn.headers: return None

        parts = conn.headers["Authorization"].split(" ")
        if len(parts) != 2: raise AuthenticationError("Invalid authorization header")
        scheme, strtoken = parts

        if scheme.lower() != 'bearer': raise AuthenticationError("Invalid authorization header")

        try:
            token = Token.decode(strtoken)
        except JWTDecodeError as ex:
            raise AuthenticationError("Invalid or expired token")

        return (AuthCredentials(["authenticated"]), JWTUser(token))


class Routes:
    router: APIRouter
    database: Database
    app: FastAPI

    def __init__(self, db: Database):
        self.db = db

        self.router = APIRouter()
        self.app = FastAPI(
            title="Summarily",
            description="""
            Summarily is a service that provides a set of tools to help you summarize articles, videos, and shorten URLs.
            """,
            summary="Summarily API",
            version="0.0.1",
            contact={
                "name": "Someone",
                "email": "someone@example.com"
            }
        )

        self.router.add_api_route("/google", self.google_route, methods=["GET"])
        self.router.add_api_route("/google/callback", self.google_callback_route, methods=["GET"])
        self.router.add_api_route("/auth/register", self.register_route, methods=["POST"])
        self.router.add_api_route("/auth/login", self.login_route, methods=["POST"])
        self.router.add_api_route("/auth/refresh", self.refresh_route, methods=["POST"])

        self.router.add_api_route("/summarize/article", self.summarize_article_route, methods=["POST"])
        self.router.add_api_route("/summarize/video", self.summarize_video_route, methods=["POST"])
        self.router.add_api_route("/shorten", self.shorten_route, methods=["POST"])

        self.app.include_router(self.router)
        self.app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())


    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def google_route(self, request: Request):
        """
        Redirects to Google OAuth.
        """
        return google(request=request)

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def google_callback_route(self, request: Request):
        """
        Handles the callback from Google OAuth.
        """
        return google_callback(request=request)

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def register_route(self, form_data: Register):
        """
        Registers a new user account with an email and password.
        """
        return register(form_data.email, form_data.password, form_data.full_name)

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def login_route(self, form_data: Login):
        """
        Logins into a user account with an email and password.
        """
        print(form_data)
        return login(form_data.email, form_data.password)

    @requires(["authenticated"])
    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def refresh_route(self, request: Request):
        """
        Generates a new JWT token for the user.
        """
        return f'<h1>Get New Token Page</h1>'


    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def shorten_route(self, form_data: Summarize):
        """
        Shortens a URL.
        """
        return f'<h1>Shorten Page</h1>'


    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def summarize_article_route(self, form_data: Summarize):
        """
        Summerize an article from a URL.
        """
        return f"todo"


    @requires(["authenticated"])
    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def summarize_video_route(self, request: Request, form_data: Summarize):
        """
        Summerize a video from a URL.
        """
        return f"todo"
