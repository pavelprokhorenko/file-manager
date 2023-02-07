from fastapi.applications import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import BackendSettings, settings
from uvicorn import run


class Service:
    __slots__ = ("_settings", "_asgi_app")

    def __init__(self, backend_settings: BackendSettings) -> None:
        """
        Initiation ASGI app.
        """
        self._settings = backend_settings

        middleware = [
            Middleware(
                CORSMiddleware,
                allow_origins=self._settings.ALLOWED_ORIGINS,
                allow_credentials=True,
                allow_methods=self._settings.ALLOWED_METHODS,
                allow_headers=self._settings.ALLOWED_HEADERS,
            ),
        ]

        self._asgi_app = FastAPI(middleware=middleware)

    def get_app(self) -> FastAPI:
        """
        Get ASGI app.
        """
        return self._asgi_app

    def serve(self, path_to_app: str) -> None:
        """
        Start service.
        """
        if self._settings.DEBUG:
            run(
                path_to_app,
                host=self._settings.SERVER_HOST,
                port=self._settings.SERVER_PORT,
                reload=True,
                use_colors=True,
                debug=True,
            )
        else:
            run(
                path_to_app,
                host=self._settings.SERVER_HOST,
                port=self._settings.SERVER_PORT,
                workers=self._settings.SERVER_WORKERS,
            )


service = Service(backend_settings=settings)
