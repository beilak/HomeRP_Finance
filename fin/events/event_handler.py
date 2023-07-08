"""Event Handler"""
from abc import ABC, abstractmethod
import aio_pika


class EventHandler(ABC):
    """Event Handler abstract"""

    @abstractmethod
    async def run(self, msg: aio_pika.IncomingMessage):
        """Run handler of message"""
