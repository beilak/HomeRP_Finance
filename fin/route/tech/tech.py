"""Tech endpoints"""

from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide
from fin.containers import FinContainer
from fin.route.oauth import oauth_check
from fin.models.common import UserProfile
from fin.controllers.tech.tech import TechService


tech_router: APIRouter = APIRouter()


@tech_router.get(
    "/tech/{target_cnt_id}/fingerprint",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
@inject
async def get_target_records(
        target_cnt_id: int,
        tech_service: TechService = Depends(Provide[FinContainer.tech_service]),
        user_profile: UserProfile = Depends(oauth_check),
) -> str:
    """Return fingerprint for Records of Target"""

    return await tech_service.get_target_fingerprint(
        unit_id=user_profile.unit_id,
        target_cnt_id=target_cnt_id,
    )
