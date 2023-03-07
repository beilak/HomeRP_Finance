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

    async def create(self, cr_target_cnt: TargetCntRequestModel) -> TargetCnt:
        """Create Target Cnt"""
        if await self._repository.is_target_name_exist(cr_target_cnt.name) is True:
            raise TargetCntExist(cr_target_cnt.name)
        return await self._repository.add(TargetCnt(**cr_target_cnt.dict()))

    async def get_targets_cnt(self, offset=0, limit=100):
        """Read targets Cnt"""
        result = await self._repository.get_objects(offset=offset, limit=limit)
        users = []
        for user in result:
            users.append(user[0])
        return users

    async def get_target_cnt(self, target_cnt_id):
        """Read target Cnt detail"""
        return await self._repository.get_object(trg_cnt_id=target_cnt_id)
