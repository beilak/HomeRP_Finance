"""Service for Tech"""
import json
from redis.asyncio import BlockingConnectionPool, Redis
from fin.controllers.service import Service
import hashlib
from fin.models.target import TargetResponseModel
from fin.adapters.repository.target import TargetRepository
import logging
import aio_pika


class TechService:
    """Tech Service"""

    def __init__(
            self,
            repository: TargetRepository,
            redis_auth: dict,
            mq: dict,
    ):
        self._redis_auth: dict = redis_auth
        self.__pool = BlockingConnectionPool(
            host=self._redis_auth['host'],
            port=self._redis_auth['port'],
            password=self._redis_auth['pwd'],
            decode_responses=True,
        )
        self._repository: TargetRepository = repository
        self._mq_dsn = f"amqp://{mq['mq_user']}:{mq['mq_pwd']}@{mq['mq_host']}/"
        self._mq_exchange = mq["mq_exchange"]

    def __await__(self):
        return self.init().__await__()

    async def init(self):
        # ToDo inject Redis
        self._pool = await Redis(connection_pool=self.__pool)

        # ToDo Declarate exchange should not be here
        async with await aio_pika.connect_robust(self._mq_dsn) as conn:
            channel = await conn.channel()
            await channel.declare_exchange(
                self._mq_exchange, aio_pika.ExchangeType.DIRECT,
            )

        return self

    async def get_target_fingerprint(self, unit_id: str, target_cnt_id: int) -> str:
        """Read target fingerprint"""
        # ToDo check is user possible to get fingerprint from this TargetCnt

        result = await self._repository.get_objects(
            unit_id=unit_id,
            targets_cnt_id=[target_cnt_id],
        )

        targets = []
        for target in result:
            targets.append(
                TargetResponseModel(**target[0].__dict__),
            )
        targets_str = json.dumps(targets, default=str,)
        return hashlib.sha256(targets_str.encode('utf-8')).hexdigest()

    async def set_req_processed(self, req_id: str) -> None:
        await self._pool.set(name=req_id, value=req_id)

    async def is_req_processed(self, req_id: str) -> bool:
        proc_id = await self._pool.get(name=req_id)
        return True if proc_id == req_id else False

    async def check_db_connection(self) -> None:
        await self._repository.is_obj_exist(1)

    async def check_rabbit(self) -> None:
        # ToDo Replace to EventController
        async with await aio_pika.connect_robust(self._mq_dsn, timeout=1) as conn:
            await conn.channel()

    async def check_redis(self) -> None:
        await self.is_req_processed("nil")


async def init_tech_service(
        repository: TargetRepository,
        redis_auth: dict,
        mq: dict,
) -> TechService:
    return await TechService(
        repository,
        redis_auth,
        mq,
    )