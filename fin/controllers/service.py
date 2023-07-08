"""Service for Target Center"""
from fin.adapters.repository import Repository
from abc import ABC, abstractmethod
from typing import Any


class Service: #(ABC):
    """Target Center Service"""

    def __init__(self, repository: Repository) -> None:
        """Init."""
        self._repository = repository

    # @abstractmethod
    async def create(self, *args, **kwargs) -> Any:
        """Create object"""
        raise NotImplementedError
