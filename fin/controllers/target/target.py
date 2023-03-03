"""Service for Target Center"""
from fin.models.target import TargetRequestModel
from fin.adapters.db.db_schemas.target.target import Target
from fin.controllers.service import Service


class TargetService(Service):
    """Target Center Service"""

    async def create(self, cr_target: TargetRequestModel) -> Target:
        """Create Target Cnt"""
        return await self._repository.add(Target(**cr_target.dict()))

    async def get_targets(self, targets_cnt_id: list, offset=0, limit=100):
        """Read targets Cnt"""
        result = await self._repository.get_objects(targets_cnt_id=targets_cnt_id, offset=offset, limit=limit)
        users = []
        for user in result:
            users.append(user[0])
        return users

    async def get_target(self, target_id):
        """Read target Cnt detail"""
        return await self._repository.get_object(unit_id=target_id)
