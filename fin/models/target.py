"""Target models"""

from pydantic import BaseModel
from decimal import Decimal


class TargetCntResponseModel(BaseModel):
    target_cnt_id: int
    # unit_id: str
    # user_login: str
    name: str
    description: str
    value: Decimal
    currency: str
    # current_value: Decimal


class TargetCntRequestModel(BaseModel):
    name: str
    description: str
    value: Decimal
    currency: str
    init_value: Decimal
    init_currency: str


class TargetResponseModel(BaseModel):
    target_id: int
    target_cnt_id: int
    user_login: str


class TargetRequestModel(BaseModel):
    target_cnt_id: int
    user_login: str
    value: Decimal
    currency: str
