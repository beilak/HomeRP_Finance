from sqlalchemy import select
from fin.adapters.db.db_schemas.db_model import Target
from fin.adapters.repository.target.error import TargetNotFoundError
from fin.adapters.repository.repository import Repository


class TargetRepository(Repository):

    def __init__(self, db_session) -> None:
        """Init."""
        self._db_session = db_session

    async def add(self, target: Target):
        """Add new Target"""
        async with self._db_session() as session:
            session.add(target)
            await session.commit()
            await session.refresh(target)
        return target

    async def is_obj_exist(self, trg_id: int):
        """Checking is target exist"""
        try:
            target = await self.get_object(trg_id)
            if target:
                return True
        except TargetNotFoundError:
            return False
        return False

    async def get_object(self, trg_id: int):
        """Get target info"""
        async with self._db_session() as session:
            targets = await session.execute(
                select(Target).filter(
                    Target.target_id == trg_id
                )
            )
            target = targets.fetchone()
            if not target:
                raise TargetNotFoundError(trg_id)
            else:
                return target[0]

    async def get_objects(self, unit_id: str, targets_cnt_id: list, offset=0, limit=100):
        """Get all targets"""
        async with self._db_session() as session:
            statement = select(
                Target,
            ).filter(
                Target.target_cnt_id.in_(targets_cnt_id),
            ).offset(offset).limit(limit)
            result = await session.execute(statement)
            return result.all()
