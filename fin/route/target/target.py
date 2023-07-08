"""Target and Target Cneter Router"""

from fastapi import APIRouter, Depends, status, Header
from typing import List
from dependency_injector.wiring import inject, Provide
from fin.models import TargetResponseModel, TargetRequestModel
from fin.containers import FinContainer
from fin.controllers.target import TargetService
from fin.controllers.tech.tech import TechService
from fin.route.oauth import oauth_check
from fin.models.common import UserProfile
from fin.exceptions import NoMatchError


target_router: APIRouter = APIRouter()


@target_router.post(
    "/targets/{target_cnt_id}/records",
    status_code=status.HTTP_201_CREATED,
    response_model=TargetResponseModel,
)
@inject
async def create_target_record(
        target_cnt_id: int,
        target: TargetRequestModel,
        if_match: str = Header(),
        target_service: TargetService = Depends(Provide[FinContainer.target_service]),
        tech_service: TechService = Depends(Provide[FinContainer.tech_service]),
        user_profile: UserProfile = Depends(oauth_check),
) -> TargetResponseModel:
    """Post Target Center"""

    fingerprint = await tech_service.get_target_fingerprint(
        unit_id=user_profile.unit_id, target_cnt_id=target_cnt_id,
    )

    if fingerprint != if_match:
        raise NoMatchError

    target_record = await target_service.create(
        cr_target=target,
        target_cnt_id=target_cnt_id,
        user=user_profile.login,
        unit_id=user_profile.unit_id,
    )

    return TargetResponseModel(**target_record.__dict__)


@target_router.get(
    "/targets/{target_cnt_id}/records",
    status_code=status.HTTP_200_OK,
    response_model=List[TargetResponseModel],
)
@inject
async def get_target_records(
        target_cnt_id: int,
        skip: int = 0,
        limit: int = 100,
        target_service: TargetService = Depends(Provide[FinContainer.target_service]),
        user_profile: UserProfile = Depends(oauth_check),
) -> List[TargetResponseModel]:
    """Return list of Targets by Target Cnt"""
    targets = await target_service.get_targets(
        unit_id=user_profile.unit_id, targets_cnt_id=[target_cnt_id], offset=skip, limit=limit,
    )
    target_out = []
    for target in targets:
        target_out.append(TargetResponseModel(**target.__dict__))
    return target_out
