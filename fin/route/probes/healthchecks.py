import logging

from fastapi import APIRouter, Depends, Response
from fin.containers import FinContainer
from dependency_injector.wiring import Provide, inject
from fin.controllers.tech.tech import TechService

checker_router: APIRouter = APIRouter()


@checker_router.get("/health", status_code=200)
async def health_check() -> None:
    """health check"""
    return None


@checker_router.get("/readiness", status_code=200)
@inject
async def readiness_check(
    response: Response,
    tech_service: TechService = Depends(Provide[FinContainer.tech_service])
) -> None:
    """readiness check"""
    try:
        await tech_service.check_db_connection()
        await tech_service.check_redis()
        await tech_service.check_rabbit()
    except BaseException as e:
        # ToDo Fix Exc type
        logging.error(f"Error in probes {e}")
        response.status_code = 500
        response.body = str(e)

    return None
