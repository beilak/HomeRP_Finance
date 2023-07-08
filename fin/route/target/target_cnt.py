"""Target and Target Cneter Router"""

from fastapi import APIRouter, Depends, status, HTTPException, Header, Response
from typing import List
from dependency_injector.wiring import inject, Provide
from fin.models import TargetCntResponseModel, TargetCntRequestModel, TargetResponseModel, TargetRequestModel
from fin.containers import FinContainer
from fin.controllers.target import TargetService, TargetCntService
from fin.adapters.repository.target.error import TargetCntExist
from fin.route.oauth import oauth_check
from fin.models.common import UserProfile


target_cnt_router: APIRouter = APIRouter()


@target_cnt_router.post(
    "/targets",
    status_code=status.HTTP_201_CREATED,
    response_model=TargetCntResponseModel,
)
@inject
async def create_target_cnt(
        response: Response,
        target: TargetCntRequestModel,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
        user_profile: UserProfile = Depends(oauth_check),
) -> TargetCntResponseModel:
    """Post Target Center"""
    try:
        target = await target_cnt_service.create(
            target, user=user_profile.login, unit_id=user_profile.unit_id,
        )
    except TargetCntExist:
        response.status_code = 200
        target = await target_cnt_service.get_target_by_name(
            unit_id=user_profile.unit_id,
            target_cnt_name=target.name,
        )

    created_target_dict = target.__dict__
    created_target_dict["currency"] = str(created_target_dict["currency"])

    return TargetCntResponseModel(**created_target_dict)


@target_cnt_router.get(
    "/targets",
    status_code=status.HTTP_200_OK,
    response_model=List[TargetCntResponseModel],
)
@inject
async def get_targets_cnt(
        skip: int = 0,
        limit: int = 100,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
        user_profile: UserProfile = Depends(oauth_check),
) -> List[TargetCntResponseModel]:
    """Return list of Targets Center"""
    targets = await target_cnt_service.get_targets_cnt(
        unit_id=user_profile.unit_id, offset=skip, limit=limit,
    )
    target_out = []
    for target in targets:
        target_cnt_dict = target.__dict__
        target_cnt_dict["currency"] = str(target_cnt_dict["currency"])
        target_out.append(TargetCntResponseModel(**target_cnt_dict))
    return target_out


@target_cnt_router.get(
    "/targets/{target_cnt_id}",
    status_code=status.HTTP_200_OK,
    response_model=TargetCntResponseModel,
)
@inject
async def get_target_cnt(
        target_cnt_id: int,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
        user_profile: UserProfile = Depends(oauth_check),
) -> TargetCntResponseModel:
    """Return list of Targets Centers"""
    target_cnt = await target_cnt_service.get_target_cnt(
        unit_id=user_profile.unit_id,
        target_cnt_id=target_cnt_id,
    )
    target_cnt_dict = target_cnt.__dict__
    target_cnt_dict["currency"] = str(target_cnt_dict["currency"])
    return TargetCntResponseModel(**target_cnt_dict)
