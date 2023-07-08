"""Receiver Event from MQ"""
import asyncio
import aio_pika
import aiormq #exceptions.ChannelInvalidStateError
import typing as tp
from fin.events.event_handler import EventHandler
from fin.events.error import EventHandlerError
import logging
from fin.controllers.tech.tech import TechService

HANDLER_NAME: tp.TypeAlias = str
HANDLER: tp.TypeAlias = EventHandler


class EventReceiver:

    def __init__(
            self, mq_host: str, mq_user: str, mq_pwd: str, queue_name: str,
            tech_service: TechService,
            handlers: dict[HANDLER_NAME: HANDLER],
    ):
        self._connection = None
        self._mq_dsn = f"amqp://{mq_user}:{mq_pwd}@{mq_host}/"
        self._queue_name = queue_name
        self._handlers: dict[HANDLER_NAME: HANDLER] = handlers
        self._tech_service = tech_service

    def __str__(self) -> str:
        return "EventReceiver..."   # ToDo move to Name and inject

    def run(self):
        asyncio.create_task(self._run())

    async def _run(self):
        while True:
            try:
                await asyncio.sleep(0.1)
                await self._run_receive_msg()
            except TimeoutError as time_e:
                logging.error(msg=f"Exception on {str(self)}. {time_e = } {type(time_e) = }")
            except asyncio.exceptions.CancelledError or aiormq.exceptions.ChannelInvalidStateError:
                break
            except BaseException as e:
                logging.error(msg=f"Exception on {str(self)}. {e = } {type(e) = }")
                break

    async def _run_receive_msg(self) -> None:
        async with await aio_pika.connect_robust(self._mq_dsn, timeout=0.1) as conn:
            channel = await conn.channel()
            queue = await channel.declare_queue(self._queue_name, durable=True)
            await queue.bind(
                exchange="hrp",
                routing_key="org_event",    # ToDo to Config
            )
            async with queue.iterator() as queue_iter:
                message: aio_pika.IncomingMessage
                async for message in queue_iter:
                    try:
                        async with message.process():
                            x_req_id = message.headers.get("X-REQ-ID")
                            logging.error(f"> {x_req_id = }")
                            is_req_processed = await self._tech_service.is_req_processed(req_id=x_req_id)
                            if not is_req_processed:
                                event_name = message.headers.get("EVENT_NAME")
                                handler = self._handlers.get(event_name)
                                await handler.run(message)
                                await self._tech_service.set_req_processed(req_id=x_req_id)
                    except EventHandlerError as e:
                        logging.error(f"Exception on {str(self)}. {e = }")
