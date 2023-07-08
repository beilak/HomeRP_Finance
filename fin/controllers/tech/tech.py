"""Service for Tech"""
import json
from redis.asyncio import BlockingConnectionPool, Redis
from fin.controllers.service import Service
import hashlib
from fin.models.target import TargetResponseModel
from fin.adapters.repository.target import TargetRepository
import logging


class TechService:
    """Tech Service"""

    def __init__(
            self,
            repository: TargetRepository,
            redis_auth: dict,
    ):
        self._redis_auth: dict = redis_auth
        self.__pool = BlockingConnectionPool(
            host=self._redis_auth['host'],
            port=self._redis_auth['port'],
            password=self._redis_auth['pwd'],
            decode_responses=True,
        )
        self._repository: TargetRepository = repository

    def __await__(self):
        return self.init().__await__()

    async def init(self):
        self._pool = await Redis(connection_pool=self.__pool)
        print("a init")
        print(self._pool)
        return self

    # async def get_redis(self) -> Redis:
    #     # ToDo Add Async init and inject redis
    #     return await redis.Redis(
    #         host=self._redis_auth['host'],
    #         port=self._redis_auth['port'],
    #         password=self._redis_auth['pwd'],
    #     ).connection

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
        # return await self._repository.get_targets(unit_id=target_id)

    async def set_req_processed(self, req_id: str) -> None:
        # cache = await self.get_redis()
        print("set")
        await self._pool.set(name=req_id, value=req_id)

    async def is_req_processed(self, req_id: str) -> bool:
        # cache = await self.get_redis()
        proc_id = await self._pool.get(name=req_id)
        return True if proc_id == req_id else False


async def init_tech_service(
        repository: TargetRepository,
        redis_auth: dict,
) -> TechService:
    return await TechService(
        repository,
        redis_auth
    )