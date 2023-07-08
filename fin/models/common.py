"""Common for models"""

from moneyed import Money as BaseMoney
from pydantic import BaseModel


class Money(BaseMoney):
    """Money type """
    def __composite_values__(self):
        return self.amount, self.currency.code


class UserProfile(BaseModel):
    login: str
    unit_id: str
