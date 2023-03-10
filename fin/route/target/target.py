"""Target and Target Cneter Router"""

from fastapi import APIRouter, Depends, status, HTTPException, Security
from typing import List
from dependency_injector.wiring import inject, Provide
from fin.models import TargetCntResponseModel, TargetCntRequestModel, TargetResponseModel, TargetRequestModel
from fin.containers import FinContainer
from fin.controllers.target import TargetService, TargetCntService
from fin.route.oauth import oauth_check


target_router: APIRouter = APIRouter()


@target_router.post(
    "/unit/{unit_id}/target/{target_cnt_id}/record",
    status_code=status.HTTP_201_CREATED,
    response_model=TargetResponseModel,
)
@inject
async def create_target_record(
        unit_id: str,
        target: TargetRequestModel,
        target_service: TargetService = Depends(Provide[FinContainer.target_service]),
) -> TargetResponseModel:
    """Post Target Center"""
    created_target_record = await target_service.create(target)
    return TargetResponseModel(**created_target_record.__dict__)


@target_router.get(
    "/unit/{unit_id}/target/{target_cnt_id}/records",
    status_code=status.HTTP_200_OK,
    response_model=List[TargetResponseModel],
)
@inject
async def get_target_records(
        unit_id: str,
        target_cnt_id: int,
        skip: int = 0,
        limit: int = 100,
        target_service: TargetService = Depends(Provide[FinContainer.target_service]),
) -> List[TargetResponseModel]:
    """Return list of Targets by Target Cnt"""
    targets = await target_service.get_targets(
        targets_cnt_id=[target_cnt_id], offset=skip, limit=limit
    )
    target_out = []
    for target in targets:
        target_out.append(TargetResponseModel(**target.__dict__))
    return target_out
