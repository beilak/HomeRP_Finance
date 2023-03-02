from sqlalchemy import select
from fin.adapters.db.db_schemas.target.target_cnt import TargetCnt
from fin.adapters.target.error import TargetCntNotFoundError


class TargetCntRepository:

    def __init__(self, db_session) -> None:
        """Init."""
        self._db_session = db_session

    async def add(self, target_cnt: TargetCnt):
        """Add new Target Center"""
        async with self._db_session() as session:
            session.add(target_cnt)
            await session.commit()
            await session.refresh(target_cnt)
        return target_cnt

    async def is_trg_cnt_exist(self, trg_cnt_id: int):
        """Checking is target center exist"""
        try:
            target_cnt = await self.get_target_cnt(trg_cnt_id)
            if target_cnt:
                return True
        except TargetCntNotFoundError:
            return False
        return False

    async def get_target_cnt(self, trg_cnt_id: int):
        """Get target center info"""
        async with self._db_session() as session:
            targets_cnt = await session.execute(select(TargetCnt).filter(TargetCnt.target_cnt_id == trg_cnt_id))
            target_cnt = targets_cnt.fetchone()
            if not target_cnt:
                raise TargetCntNotFoundError(trg_cnt_id)
            else:
                return target_cnt[0]

    async def get_targets_cnt(self, offset=0, limit=100):
        async with self._db_session() as session:
            statement = select(TargetCnt).offset(offset).limit(limit)
            result = await session.execute(statement)
            return result.all()
