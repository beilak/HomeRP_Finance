"""Service for Target Center"""
from fin.models.target import TargetRequestModel
from fin.adapters.db.db_schemas.db_model import Target
from fin.controllers.service import Service


class TargetService(Service):
    """Target Center Service"""

    async def create(self, cr_target: TargetRequestModel, target_cnt_id: int, user: str, unit_id: str) -> Target:
        """Create Target Cnt"""
        # ToDo check is user possible to add to this TargetCnt

        return await self._repository.add(
            Target(
                **{
                    **cr_target.dict(),
                    "target_cnt_id": target_cnt_id,
                    "user_login": user,
                }
            ),
        )

    async def get_targets(self, unit_id: str, targets_cnt_id: list, offset=0, limit=100):
        """Read targets Cnt"""
        # ToDo check is user possible to get from this TargetCnt

        result = await self._repository.get_objects(
            unit_id=unit_id, targets_cnt_id=targets_cnt_id, offset=offset, limit=limit
        )
        targets = []
        for target in result:
            targets.append(target[0])
        return targets

    async def get_target(self, target_id):
        """Read target Cnt detail"""
        # ToDo check is user possible to get from this TargetCnt

        return await self._repository.get_object(unit_id=target_id)
