"""Target and Target Cneter Router"""

from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from dependency_injector.wiring import inject, Provide
from fin.models import TargetCntResponseModel, TargetCntRequestModel
from fin.containers import FinContainer
from fin.controllers.target import TargetService, TargetCntService


target_router: APIRouter = APIRouter()


@target_router.get(
    "/targets",
    status_code=status.HTTP_200_OK,
    response_model=List[TargetCntResponseModel],
)
@inject
async def get_targets_cnt(
        skip: int = 0,
        limit: int = 100,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
) -> List[TargetCntResponseModel]:
    """Return list of Targets Center"""
    targets = await target_cnt_service.get_targets_cnt(offset=skip, limit=limit)
    target_out = []
    for target in targets:
        target_out.append(TargetCntResponseModel(**target.__dict__))
    return target_out


@target_router.get(
    "/target/{target_id}",
    status_code=status.HTTP_200_OK,
    response_model=TargetCntResponseModel,
)
@inject
async def get_target_cnt(
        target_cnt_id: int,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
) -> TargetCntResponseModel:
    """Return list of Targets Centers"""
    target_cnt = await target_cnt_service.get_target_cnt(target_cnt_id=target_cnt_id)
    return TargetCntResponseModel(**target_cnt.__dict__)


@target_router.post(
    "/target",
    status_code=status.HTTP_201_CREATED,
    response_model=TargetCntResponseModel,
)
@inject
async def create_unit(
        target: TargetCntRequestModel,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
) -> TargetCntResponseModel:
    """Post Target Center"""
    created_target = await target_cnt_service.create(target)
    return TargetCntResponseModel(**created_target.__dict__)
