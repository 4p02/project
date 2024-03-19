from typing import Optional, Tuple, Annotated

from fastapi import APIRouter, Depends, Header, Request, FastAPI, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

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
from backend.misc import check_valid_url

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

        # Because fastapi is designed very well, it flagrantly ignores any
        # starlette middleware that the user defines, and decides on it's own
        # accord to fucking reimplement the entirety of AuthenticationBackend,
        # with no recourse for backwards compatability, because fuck you that's
        # why. Using any middleware means it's functionally excluded from
        # swagger and openapi. So, define a fucking dummy middleware that does
        # fuck-all for authentication to appease the silly swagger gods, all so
        # a fucking "Authorize" popup shows on swagger. Fuck this shit man.
        def fastapi_fake_auth(x: Annotated[Header, Security(HTTPBearer(auto_error=False))]):
            return x

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
            },
            dependencies=[Depends(fastapi_fake_auth)],
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

        # there's no way to use lambda type annotations, and on_error is kwargs
        def auth_middleware_handle_err(conn: HTTPConnection, ex: Exception):
            return HTTPException(401, str(ex))

        self.app.add_middleware(
            AuthenticationMiddleware,
            backend=JWTAuthBackend(),
            on_error=auth_middleware_handle_err,
        )


    def get_app(self) -> FastAPI:
        """
        Return the fast API instance.
        @return: FastAPI
        """
        return self.app

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def google_route(self, request: Request):
        """
        Redirects to Google OAuth.
        @param request: Request to authorize redirect to the Google OAuth.
        @return: RedirectResponse
        """
        return google(request=request)


    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def google_callback_route(self, request: Request):
        """
        Handles the callback from Google OAuth.
        @param request: Request to handle the callback from Google OAuth.
        @return: RedirectResponse
        """
        return google_callback(db=self.db, request=request)


    # @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    async def register_route(self, form: Register):
        """
        Registers a new user account with an email, password, fullname.
        @param form: Register {email: str, password: str, fullname: str}
        @return: dict with jwt {token: str}
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
        @param form: Login {email: str, password: str}
        @return: dict with jwt {token: str}
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
        # check if token is expired
        if token.is_expired():
            raise HTTPException(401, "Token is expired")
        return {"token": Token.new(token.uid).encode()}


    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def shorten_route(self, form: Summarize):
        """
        Shortens a URL. given a link to shorten
        @param form: Summarize {url: str}
        @return: dict with {shortLink: str}
        """

        if not check_valid_url(form.url):
            raise HTTPException(400, "Invalid URL")

        return {"shortLink": "todo"}


    def summarize_article_route(self, form: Summarize):
        """
        Summerize an article from a URL.
        """
        url = form.url
        
        
        if not check_valid_url(url):
            raise HTTPException(400, "Invalid URL")
        
        # add details to database
        return JSONResponse(content={"summary": "todo", "shortLink": "todo"}, headers={"Access-Control-Allow-Origin": "*", "content-type": "application/json"})


    @requires(["authenticated"])
    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def summarize_video_route(self, request: Request, form: Summarize):
        """
        Summerize a video from a URL.
        @param form: Summarize {url: str}
        @return: dict with {summary: str, shortLink: str}
        """
        url = form.url
        
        return JSONResponse(content={"summary": "todo", "shortLink": "todo"}, headers={"Access-Control-Allow-Origin": "*", "content-type": "application/json"})
