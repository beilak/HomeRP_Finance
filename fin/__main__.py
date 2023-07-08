from fin.containers import FinContainer
from fin.config import Settings
from typing import Final
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fin.exceptions import valid_except_handler, http_except_handler
from fin.route import target_router, target_cnt_router, tech_router
# from fastapi.middleware.cors import CORSMiddleware
from fin.route.oauth import oauth_check
from dependency_injector.wiring import Provide, inject
from fin.events.event_receiver import EventReceiver
from starlette_prometheus import metrics, PrometheusMiddleware


FIN_APP: FastAPI


@inject
async def run_event_receiver(
        event_receiver: EventReceiver = Provide[FinContainer.event_receiver],
        # tech_service: EventReceiver = Provide[FinContainer.tech_service],
) -> None:
    event_receiver.run()


async def service_startup() -> None:
    """ Init service """
    settings: Settings = Settings()
    container: Final[FinContainer] = FinContainer.create_container(settings)
    container.init_resources()
    FIN_APP.container = container

    await run_event_receiver()
    # container._target_repository()
    # container.tech_service()
    # await container.event_receiver().run()


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
    swagger_ui_init_oauth={
        "clientId": "HomeRP_UI"
    },
    dependencies=[
        Depends(oauth_check)
    ]
)

# ORIGINS = [
#     "https://cdn.jsdelivr.net",
#     "http://127.0.0.1:28080",
#     "http://127.0.0.1:8081",
#     "*",
# ]
#
# FIN_APP.add_middleware(
#     CORSMiddleware,
#     allow_origins=ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

FIN_APP.add_middleware(PrometheusMiddleware)

FIN_APP.include_router(target_cnt_router, prefix=_API_PREFIX, tags=["Target"])
FIN_APP.include_router(target_router, prefix=_API_PREFIX, tags=["Target flow"])
FIN_APP.include_router(tech_router, prefix=_API_PREFIX, tags=["Tech"])
FIN_APP.add_route("/metrics", metrics)

FIN_APP.add_exception_handler(RequestValidationError, valid_except_handler)
FIN_APP.add_exception_handler(StarletteHTTPException, http_except_handler)
