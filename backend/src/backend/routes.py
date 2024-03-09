from typing import Optional, Tuple

from fastapi import APIRouter, Depends, Request, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser,
    requires
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection

from jwt.exceptions import JWTDecodeError

from backend import config, logger
from backend.auth import Token, google, google_callback, login_user, register_user
from backend.db import Database
from backend.models import Login, Register, Summarize
from backend.misc import handle_and_log_exceptions
from urllib.parse import urlparse


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
        # we need this middleware to handle CORS
        self.app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
        # todo: make this output 401 or 403 instead of a generic 400
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


    # @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    async def register_route(self, form: Register):
        """
        Registers a new user account with an email and password.
        """
        user = await register_user(
            self.db,
            email=form.email, password=form.password, fullname=form.fullname
        )

        if user is not None:
            return {"token": Token.new(user["id"]).encode()}

        raise HTTPException(400, "Email is already in use.")


    # @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    async def login_route(self, form: Login):
        """
        Logins into a user account with an email and password.
        """
        if (user := await login_user(self.db, email=form.email, password=form.password)) is not None:
            return {"token": Token.new(user["id"]).encode()}

        raise HTTPException(401, "Invalid email or password.")


    @requires(["authenticated"])
    # @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def refresh_route(self, request: Request):
        """
        Renews the expiration date on a JWT token.
        """
        token: Token = request.user.token
        return {"token": Token.new(token.uid).encode()}


    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def shorten_route(self, form_data: Summarize):
        """
        Shortens a URL.
        """
        return f'<h1>Shorten Page</h1>'


    def summarize_article_route(self, form_data: Summarize):
        """
        Summerize an article from a URL.
        """
        url = form_data.url
        
        # check if url is localhost or an ip address which is not allowed for security things
        if urlparse(url).hostname in ["localhost", "127.0.0.1", "0.0.0.0"]:
            raise HTTPException(400, "Invalid URL")
        elif urlparse(url).hostname is None:
            raise HTTPException(400, "Invalid URL")
        
        print(url)
        return JSONResponse(content={"summary": "todo", "shortLink": "todo"}, headers={"Access-Control-Allow-Origin": "*", "content-type": "application/json"})


    @requires(["authenticated"])
    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def summarize_video_route(self, request: Request, form_data: Summarize):
        """
        Summerize a video from a URL.
        """
        url = form_data.url
        
        return f"todo"
