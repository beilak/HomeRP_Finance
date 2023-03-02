from sqlalchemy import select
from fin.db.db_schemas.target.target import Target
from fin.controllers.target.error import TargetNotFoundError


class TargetRepository:

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

    async def is_trg_exist(self, trg_id: int):
        """Checking is target exist"""
        try:
            target = await self.get_target(trg_id)
            if target:
                return True
        except TargetNotFoundError:
            return False
        return False

    async def get_target(self, trg_id: int):
        """Get target info"""
        async with self._db_session() as session:
            targets = await session.execute(select(Target).filter(Target.target_id == trg_id))
            target = targets.fetchone()
            if not target:
                raise TargetNotFoundError(trg_id)
            else:
                return target[0]

    async def get_targets(self, offset=0, limit=100):
        """Get all targets"""
        async with self._db_session() as session:
            statement = select(Target).offset(offset).limit(limit)
            result = await session.execute(statement)
            return result.all()
