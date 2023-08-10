from typing import NoReturn

from fastapi.applications import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from src.config.settings import settings


class Server:
    __slots__ = (
        "_settings",
        "_asgi_app",
    )

    def __init__(self) -> None:
        """
        Initiation ASGI src.
        """

        self._asgi_app = FastAPI(middleware=self._get_middleware())

    @staticmethod
    def _get_middleware() -> list[Middleware]:
        return [
            Middleware(
                CORSMiddleware,
                allow_origins=settings.ALLOWED_ORIGINS,
                allow_credentials=True,
                allow_methods=settings.ALLOWED_METHODS,
                allow_headers=settings.ALLOWED_HEADERS,
            ),
        ]

    def get_app(self) -> FastAPI:
        """
        Get ASGI src.
        """

        return self._asgi_app

    @staticmethod
    def serve(path_to_app: str) -> NoReturn:  # type: ignore[misc]
        """
        Start server.
        """

        if settings.DEBUG:
            run(
                path_to_app,
                host=settings.SERVER_HOST,
                port=settings.SERVER_PORT,
                reload=True,
                use_colors=True,
            )
        else:
            run(
                path_to_app,
                host=settings.SERVER_HOST,
                port=settings.SERVER_PORT,
                workers=settings.SERVER_WORKERS,
            )


server = Server()
