import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from auth import google, google_callback, register, login
from models import Login, Register, Summarize
from routes import Routes
from backend import config


def main():
    try:
        app = fastapi.FastAPI()
        router: fastapi.APIRouter = Routes().get_router()
        app.include_router(router)
        uvicorn.run(app, host=config.api.host, port=config.api.port)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
