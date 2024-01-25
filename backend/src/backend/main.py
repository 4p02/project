import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import backend.routes

app = fastapi.FastAPI()

def main():
    try:
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
