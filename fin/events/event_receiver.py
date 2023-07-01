"""Receiver Event from MQ"""
import asyncio
import aio_pika


class EventReceiver:

    def __init__(self, mq_host, mq_user: str, mq_pwd: str, queue_name: str):
        self._connection = None
        self._mq_dsn = f"amqp://{mq_user}:{mq_pwd}@{mq_host}/"
        self._queue_name = queue_name

    async def run(self):
        asyncio.create_task(self._run())

    async def _run(self):
        while True:
            try:
                await asyncio.sleep(0.1)
                await self._run_receive_msg()
            except BaseException:
                break

    async def _run_receive_msg(self) -> None:
        async with await aio_pika.connect_robust(self._mq_dsn, timeout=0.1) as conn:
            channel = await conn.channel()
            queue = await channel.declare_queue(self._queue_name, durable=True)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        print(message)
