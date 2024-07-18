
import asyncio
from puter import Computer


async def input_puter():
    com = Computer(0, -1, "input.txt")
    while True:
        await asyncio.sleep(0.5)
        await com.excute_next()
        print(f"{com.X}${com.Y} acc", com.ACC)


async def main():
    com = Computer(0, 0, "tis100.txt")
    while True:
        await asyncio.sleep(0.2)
        await com.excute_next()
        print(f"{com.X}${com.Y} acc", com.ACC)

loop = asyncio.new_event_loop()
input_task = loop.create_task(input_puter())
loop.run_until_complete(main())
