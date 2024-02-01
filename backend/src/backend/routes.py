from fastapi import APIRouter, Depends
from auth import api_key_auth
from summarize import summarize_from_article, summarize_from_video
from models import Login, Register, Summarize
from fastapi.middleware.cors import CORSMiddleware
from auth import google, google_callback, login, register



class Routes:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/google", self.google_route, methods=["GET"])
        self.router.add_api_route("/google/callback", self.google_callback_route, methods=["GET"])
        self.router.add_api_route("/register", self.register_route, methods=["POST"])
        self.router.add_api_route("/login", self.login_route, methods=["POST"])
        self.router.add_api_route("/get_new_token", self.get_new_token_route, methods=["POST"])
        self.router.add_api_route("/summerize/article", self.summerize_article_route, methods=["POST"], dependencies=[Depends(api_key_auth)])
        self.router.add_api_route("/summerize/video", self.summerize_video_route, methods=["POST"], dependencies=[Depends(api_key_auth)])
        self.router.add_api_route("/shorten", self.shorten_route, methods=["POST"], dependencies=[Depends(api_key_auth)])
        self.router.add_api_route("/history", self.get_history_route, methods=["GET"], dependencies=[Depends(api_key_auth)])
        pass
    def get_router(self):
        return self.router
    def google_route(self):
        return google()
    def google_callback_route(self):
        return google_callback()

    def register_route(self, form_data: Register):
        return register(form_data.email, form_data.password, form_data.full_name)

    def login_route(self, form_data: Login):
        print(form_data)
        return login(form_data.email, form_data.password)

    def get_new_token_route(self):
        return f'<h1>Get New Token Page</h1>'

    def get_history_route(self):
        return f'<h1>History Page</h1>'

    def shorten_route(self, form_data: Summarize):
        return f'<h1>Shorten Page</h1>'



    def summerize_article_route(self, form_data: Summerize):
        return summerize_from_article(form_data.url)
    def summerize_video_route(self, form_data: Summerize):
        return summerize_from_video(form_data.url)
