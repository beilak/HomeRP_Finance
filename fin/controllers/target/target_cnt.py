"""Service for Target Center"""

from fin.models.target import TargetCntRequestModel
from fin.adapters.db.db_schemas.target.target_cnt import TargetCnt
from fin.controllers.service import Service
from fin.adapters.repository.target.error import TargetCntExist
from fin.adapters.repository.target import TargetCntRepository


class TargetCntService(Service):
    """Target Center Service"""
    def __init__(self, repository: TargetCntRepository) -> None:
        """Init."""
        super().__init__(repository)
        self._repository = repository

    async def create(self, cr_target_cnt: TargetCntRequestModel, user: str, unit_id: str) -> TargetCnt:
        """Create Target Cnt"""
        if await self._repository.is_target_name_exist(cr_target_cnt.name) is True:
            raise TargetCntExist(cr_target_cnt.name)

        return await self._repository.add(
            TargetCnt(
                **cr_target_cnt.dict(),
                unit_id=unit_id,
                user_login=user,
            )
        )

    async def get_targets_cnt(self, unit_id: str, offset=0, limit=100):
        """Read targets Cnt"""
        result = await self._repository.get_objects(unit_id=unit_id, offset=offset, limit=limit)
        users = []
        for user in result:
            users.append(user[0])
        return users

    async def get_target_cnt(self, unit_id: str, target_cnt_id: int):
        """Read target Cnt detail"""
        return await self._repository.get_object(
            unit_id=unit_id,
            trg_cnt_id=target_cnt_id,
        )

    async def get_target_by_name(self, unit_id: str, target_cnt_name: str):
        """Read target Cnt detail"""
        return await self._repository.get_object_by_name(
            unit_id=unit_id,
            trg_cnt_name=target_cnt_name,
        )

    async def init_defaulter_target_cnt(self, unit_id: str) -> None:
        # ToDo Implement
        print("ToDo >>>>")
