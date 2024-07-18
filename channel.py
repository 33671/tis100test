import asyncio


class DataChannel:
    Data: int = None
    condition: asyncio.Condition

    is_sending = False

    is_reading = False

    def __init__(self) -> None:
        self.condition = asyncio.Condition()

    async def send(self, item: int):
        self.is_sending = True
        async with self.condition:
            self.Data = item
            self.condition.notify_all()
            # wait til sent data read complete
            while self.Data is not None:
                await self.condition.wait()
        self.is_sending = False

    async def read(self) -> int:
        self.is_reading = True
        async with self.condition:
            # wait til data is provided
            while self.Data is None:
                await self.condition.wait()
            item = self.Data
            self.Data = None
            # notify reading complete
            self.condition.notify_all()
        self.is_reading = False
        return item