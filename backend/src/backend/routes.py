from fastapi import APIRouter, Depends, Request, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend import config
from backend.auth import api_key_auth, google, google_callback, login, register
from backend.db import Database
from backend.models import Login, Register, Summarize
from backend.misc import handle_and_log_exceptions


class Routes:
    router: APIRouter
    database: Database
    app: FastAPI

    def __init__(self, db: Database):
        self.db = Database

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
        self.router.add_api_route("/register", self.register_route, methods=["POST"])
        self.router.add_api_route("/login", self.login_route, methods=["POST"])
        self.router.add_api_route("/get_new_token", self.get_new_token_route, methods=["POST"])

        self.router.add_api_route("/summarize/article", self.summarize_article_route, methods=["POST"], dependencies=[Depends(api_key_auth)])
        self.router.add_api_route("/summarize/video", self.summarize_video_route, methods=["POST"], dependencies=[Depends(api_key_auth)])
        self.router.add_api_route("/shorten", self.shorten_route, methods=["POST"], dependencies=[Depends(api_key_auth)])
        self.app.include_router(self.router)
        self.app.add_middleware(SessionMiddleware, secret_key=config.auth.jwt_secret)

    
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

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def get_new_token_route(self):
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

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def summarize_video_route(self, form_data: Summarize):
        """
        Summerize a video from a URL.
        """
        return f"todo"
