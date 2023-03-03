from abc import ABC, abstractmethod
from typing import Any


class Repository(ABC):

    @abstractmethod
    async def is_obj_exist(self, *args, **kwargs) -> bool:
        ...

    @abstractmethod
    async def add(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    async def get_objects(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    async def get_object(self, *args, **kwargs) -> Any:
        ...
