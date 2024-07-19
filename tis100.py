
import asyncio
from puter import Computer
loop = asyncio.new_event_loop()


async def input_puter():
    com = Computer(1, -1)
    for i in range(100):
        await com.block_waiting_send(i, "down")


async def output_puter():
    com = Computer(2, 3)
    with open("out.txt", "w") as f:
        while True:
            out_int = await com.block_waiting_for_data_from("up")
            f.write(str(out_int) + "\n")
            f.flush()
            print("Output Received:", out_int)


async def run_computer(com: Computer):
    while True:
        # await asyncio.sleep(1)
        await com.excute_next()


def load_and_run(x: int, y: int, program: str):
    com = Computer(x, y, program)
    return loop.create_task(run_computer(com))


async def main():
    load_and_run(1, 0, "MOV UP ANY")
    load_and_run(2, 0, "MOV ANY ANY")
    load_and_run(2, 1, """
MOV ANY ACC
ADD ACC
MOV ACC DOWN 
        """)
    load_and_run(2, 2, "MOV ANY DOWN")


loop.create_task(input_puter())
loop.create_task(main())
loop.run_until_complete(output_puter())
