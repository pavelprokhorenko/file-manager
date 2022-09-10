from os import system

from fastapi.applications import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from settings import Settings, settings


class Service:
    def __init__(self, service_settings: Settings) -> None:
        """
        Initiation ASGI app.
        """
        self.settings = service_settings

        middleware = [
            Middleware(
                CORSMiddleware,
                allow_origins=settings.service.origins,
                allow_credentials=True,
                allow_methods=["POST"],
                allow_headers=["*"],
            ),
        ]

        self.main_app = FastAPI(middleware=middleware)

    def get_app(self) -> FastAPI:
        """
        Get ASGI app.
        """
        return self.main_app

    def serve(self, path_to_app: str) -> None:
        """
        Start service.
        """
        if self.settings.service.debug:
            run(
                path_to_app,
                host=self.settings.service.host,
                port=self.settings.service.port,
                reload=True,
                use_colors=True,
                debug=True,
            )
        else:
            system(
                f"uvicorn {path_to_app} --host {self.settings.service.host} --port"
                f" {self.settings.service.port}"
            )


service = Service(service_settings=settings)
