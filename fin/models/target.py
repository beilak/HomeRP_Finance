"""Target models"""

from pydantic import BaseModel
from decimal import Decimal


class TargetResponseModel(BaseModel):
    target_id: int
    unit_id: str
    user_login: str
    target_name: str
    description: str
    target_value: Decimal
    target_currency: str
    current_value: Decimal


class TargetRequestModel(BaseModel):
    target_name: str
    description: str
    target_value: Decimal
    target_currency: str
    init_value: Decimal
    init_currency: str
