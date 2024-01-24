import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routes import index, register, login, summerize, google, google_callback, shorten

app = fastapi.FastAPI()

def main():
    try:
        app.add_api_route("/", endpoint=index, methods=["GET"])
        app.add_api_route("/auth/google", endpoint=google, methods=["GET"])
        app.add_api_route("/auth/google/callback", endpoint=google_callback, methods=["GET"])

        app.add_api_route("/auth/register", endpoint=register, methods=["POST"])
        app.add_api_route("/auth/login", endpoint=login, methods=["POST"])
        app.add_api_route("/summerize", endpoint=summerize, methods=["POST"])
        app.add_api_route("/shorten", endpoint=shorten, methods=["POST"])


        # temporary helps with CORS
        app.add_middleware(
            CORSMiddleware(
                app,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        )
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
