import fastapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from backend import config, logger
from backend.db import Database
from backend.misc import asyncio_entrypoint
from auth import google, google_callback, register, login
from models import Login, Register, Summarize
from routes import Routes


@asyncio_entrypoint
async def main():
    async with (await Database.connect()) as db:
        logger.debug("db connected")

        logger.debug("bringing up fastapi")
        app = fastapi.FastAPI(
            title="Summerily",
            description="## Summerily API",
            summary="Summerily API",
            version="0.0.1",
            contact={
                "name": "Someone",
                "email": "someone@example.com"
            }

        )
        router: fastapi.APIRouter = Routes().get_router()
        app.include_router(router)
        app.add_middleware(SessionMiddleware, secret_key=config.auth.jwt_secret)

        server = uvicorn.Server(
            uvicorn.Config(
                app=app,
                host=config.api.host,
                port=config.api.port,
                use_colors=False,
                access_log=True,
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
        )
        await server.serve()

if __name__ == "__main__":
    main()
