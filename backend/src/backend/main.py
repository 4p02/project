import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from auth import google, google_callback, register, login
from models import Login, Register, Summarize
from routes import Routes
from backend import config, logger


def main():
    try:
        logger.debug("bringing up fastapi")

        app = fastapi.FastAPI()
        router: fastapi.APIRouter = Routes().get_router()
        app.include_router(router)
        uvicorn.run(
            app=app,
            host=config.api.host,
            port=config.api.port,
            use_colors=False, access_log=True,
            log_config={
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {
                        "()": "uvicorn.logging.DefaultFormatter",
                        "fmt": "%(levelprefix)s %(message)s",
                        "use_colors": None,
                    },
                    "access": {
                        "()": "uvicorn.logging.AccessFormatter",
                        "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
                    },
                },
                "handlers": {},
                "loggers": {
                    "uvicorn": {"level": "DEBUG", "propagate": True},
                    "uvicorn.error": {"level": "DEBUG", "propagate": True},
                    "uvicorn.access": {"level": "DEBUG", "propagate": True},
                },
            }
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
