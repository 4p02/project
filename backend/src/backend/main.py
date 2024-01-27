import fastapi
from fastapi.middleware.cors import CORSMiddleware
from models import Login, Register, Summerize
from routes import Routes
from auth import google, google_callback, register, login
from constants import HOST, PORT
import uvicorn






def main():
    try:
        app = fastapi.FastAPI()
        router: fastapi.APIRouter = Routes().get_router()
        app.include_router(router)
        uvicorn.run(app, host=HOST, port=PORT)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
