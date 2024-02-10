import fastapi
import uvicorn

from backend import config, logger
from backend.db import Database
from backend.misc import asyncio_entrypoint
from backend.routes import Routes

@asyncio_entrypoint
async def main():
    async with (await Database.connect()) as db:
        logger.debug("db connected")
        logger.debug("bringing up fastapi")

        routes = Routes(database=db)
        app: fastapi.FastAPI = routes.app

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
