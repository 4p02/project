from fastapi import APIRouter, Depends, Request, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend import config
from backend.auth import api_key_auth, google, google_callback, login, register
from backend.models import Login, Register, Summarize
from backend.misc import handle_and_log_exceptions


class Routes:
    def __init__(self, db):
        self.router = APIRouter()
        self.app = FastAPI(
            title="Summerily",
            description="## Summerily API",
            summary="Summerily API",
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
        self.router.add_api_route("/history", self.get_history_route, methods=["GET"], dependencies=[Depends(api_key_auth)])
        self.app.include_router(self.router)
        self.app.add_middleware(SessionMiddleware, config.auth.jwt_secret)

    def get_app(self):
        return self.app

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def google_route(self, request: Request):
        return google(request=request)

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def google_callback_route(self, request: Request):
        return google_callback(request=request)

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def register_route(self, form_data: Register):
        return register(form_data.email, form_data.password, form_data.full_name)

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def login_route(self, form_data: Login):
        """Logins into a user account with an email and password."""
        print(form_data)
        return login(form_data.email, form_data.password)

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def get_new_token_route(self):
        return f'<h1>Get New Token Page</h1>'

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def get_history_route(self):
        return f'<h1>History Page</h1>'

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def shorten_route(self, form_data: Summarize):
        return f'<h1>Shorten Page</h1>'



    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def summarize_article_route(self, form_data: Summarize):
        return f"todo"

    @handle_and_log_exceptions(reraise=HTTPException(500, "Internal server error :("))
    def summarize_video_route(self, form_data: Summarize):
        return f"todo"
