from fin.containers import FinContainer
from fin.config import Settings
from typing import Final
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fin.exceptions import valid_except_handler, http_except_handler


FIN_APP: FastAPI


async def service_startup() -> None:
    """ Init service """
    settings: Settings = Settings()
    container: Final[FinContainer] = FinContainer.create_container(settings)
    container.init_resources()
    FIN_APP.__container = container


async def service_shutdown() -> None:
    ...


_API_VER = "v1"
_API_PREFIX = f"/api/{_API_VER}"
FIN_APP = FastAPI(
    title="Finance service",
    description="Finance service controller",
    version=_API_VER,
    docs_url=f"{_API_PREFIX}/doc",
    on_startup=[service_startup],
    on_shutdown=[service_shutdown],
    )


FIN_APP.add_exception_handler(RequestValidationError, valid_except_handler)
FIN_APP.add_exception_handler(StarletteHTTPException, http_except_handler)
