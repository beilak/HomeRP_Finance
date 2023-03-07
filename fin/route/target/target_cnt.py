"""Target and Target Cneter Router"""

from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from dependency_injector.wiring import inject, Provide
from fin.models import TargetCntResponseModel, TargetCntRequestModel, TargetResponseModel, TargetRequestModel
from fin.containers import FinContainer
from fin.controllers.target import TargetService, TargetCntService


target_cnt_router: APIRouter = APIRouter()


@target_cnt_router.post(
    "/unit/{unit_id}/target",
    status_code=status.HTTP_201_CREATED,
    response_model=TargetCntResponseModel,
)
@inject
async def create_target_cnt(
        unit_id: str,
        target: TargetCntRequestModel,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
) -> TargetCntResponseModel:
    """Post Target Center"""
    created_target = await target_cnt_service.create(target)
    created_target_dict = created_target.__dict__
    created_target_dict["currency"] = str(created_target_dict["currency"])
    return TargetCntResponseModel(**created_target_dict)


@target_cnt_router.get(
    "/unit/{unit_id}/targets",
    status_code=status.HTTP_200_OK,
    response_model=List[TargetCntResponseModel],
)
@inject
async def get_targets_cnt(
        unit_id: str,
        skip: int = 0,
        limit: int = 100,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
) -> List[TargetCntResponseModel]:
    """Return list of Targets Center"""
    targets = await target_cnt_service.get_targets_cnt(offset=skip, limit=limit)
    target_out = []
    for target in targets:
        target_cnt_dict = target.__dict__
        target_cnt_dict["currency"] = str(target_cnt_dict["currency"])
        target_out.append(TargetCntResponseModel(**target_cnt_dict))
    return target_out


@target_cnt_router.get(
    "/unit/{unit_id}/target/{target_cnt_id}",
    status_code=status.HTTP_200_OK,
    response_model=TargetCntResponseModel,
)
@inject
async def get_target_cnt(
        unit_id: str,
        target_cnt_id: int,
        target_cnt_service: TargetCntService = Depends(Provide[FinContainer.target_cnt_service]),
) -> TargetCntResponseModel:
    """Return list of Targets Centers"""
    target_cnt = await target_cnt_service.get_target_cnt(target_cnt_id=target_cnt_id)
    target_cnt_dict = target_cnt.__dict__
    target_cnt_dict["currency"] = str(target_cnt_dict["currency"])
    return TargetCntResponseModel(**target_cnt_dict)
