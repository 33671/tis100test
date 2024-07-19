import asyncio


class DataChannel:

    def __init__(self) -> None:
        self.condition = asyncio.Condition()
        self.Data: int = None
        self.is_sending = False
        self.is_reading = False

    async def send(self, item: int):
        self.is_sending = True
        async with self.condition:
            self.Data = item
            # notify time to start reading if blocking
            self.condition.notify_all()
            # wait until sent data read complete
            while self.Data is not None:
                await self.condition.wait()
        self.is_sending = False

    async def read(self) -> int:
        self.is_reading = True
        async with self.condition:
            # wait until data is provided
            while self.Data is None:
                await self.condition.wait()
            item = self.Data
            self.Data = None
            # notify reading complete
            self.condition.notify_all()
        self.is_reading = False
        return item
