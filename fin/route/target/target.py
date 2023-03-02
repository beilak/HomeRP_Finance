"""Target Router"""

from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from dependency_injector.wiring import inject, Provide
from fin.models import TargetResponseModel, TargetRequestModel


target_router: APIRouter = APIRouter()


@target_router.get(
    "/targets",
    status_code=status.HTTP_200_OK,
    response_model=List[TargetResponseModel],
)
@inject
async def get_targets(
        skip: int = 0,
        limit: int = 100,
        # target_service: TargetService = Depends(Provide[FinContainer.target_service]),
) -> List[TargetResponseModel]:
    """Return list of Targets"""
    ...


@target_router.get(
    "/target/{target_id}",
    status_code=status.HTTP_200_OK,
    response_model=TargetResponseModel,
)
@inject
async def get_target(
        target_id: int,
) -> TargetResponseModel:
    """Return list of Targets"""
    ...


@target_router.post(
    "/target",
    status_code=status.HTTP_201_CREATED,
    response_model=TargetResponseModel,
)
@inject
async def create_unit(
        target: TargetRequestModel,
) -> TargetResponseModel:
    """Post unit"""
    ...
