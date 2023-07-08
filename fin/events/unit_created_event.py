"""Handle for Event of Unit have been created"""
from fin.controllers.target import TargetCntService
from fin.events.event_handler import EventHandler
from fin.events.error import EventHandlerError
import aio_pika
import asyncio
import json


class UnitCreatedEvent(EventHandler):

    def __init__(
            self,
            target_cnt_service: TargetCntService
    ):
        self._target_cnt_service: TargetCntService = target_cnt_service

    async def run(self, msg: aio_pika.IncomingMessage):
        body: dict = json.loads(msg.body.decode())

        await self._target_cnt_service.init_defaulter_target_cnt(
            unit_id=body['unit_id'],
            login=body['admin'],
        )
