"""Handle for Event of Unit have been created"""
from fin.controllers.target import TargetCntService
from fin.events.event_handler import EventHandler
from fin.events.error import EventHandlerError
import aio_pika
import asyncio


class UnitCreatedEvent(EventHandler):

    def __int__(
            self,
            # target_cnt_service: TargetCntService
    ):
        ...
        # self._target_cnt_service: TargetCntService = target_cnt_service

    async def run(self, msg: aio_pika.IncomingMessage):
        #raise EventHandlerError
        print("proc")
        # print(msg.body.decode())
