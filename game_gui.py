import asyncio
import ctypes
import threading
from typing import Dict, List
import dearpygui.dearpygui as dpg
from node_gui import Node
from tis100 import loop
from puter import Computer
dpg.create_context()
nodes: List[List[Node]] = []
computers: Dict[str, Computer] = {}


def toggle_show():
    for x in nodes:
        for n in x:
            if not n.is_editting:
                n.switch_edit()
            else:
                n.switch_run()


def load_input():
    for y, nodes_x in enumerate(nodes):
        for x, node in enumerate(nodes_x):
            text = node.get_text()
            if text.strip() != "":
                node.switch_run()
                node.set_running_line(0)
                computer = Computer(x, y, text)
                computers[f"{x}${y}"] = computer


def step_forward_code():
    # load_input()
    for x in computers:
        puter = computers[x]
        if not puter.is_blocking():
            def done_call_back(future: asyncio.Future[Computer]) -> object:
                # print("finished")
                puter = future.result()
                nodes[puter.Y][puter.X].set_running_line(
                    puter.line_number_to_run)
                return object()
            future = asyncio.run_coroutine_threadsafe(
                puter.excute_next(), loop=loop)
            future.add_done_callback(done_call_back)


async def run_puter_forever(puter: Computer):
    while True:
        await asyncio.sleep(0.1)
        await puter.excute_next()
        nodes[puter.Y][puter.X].set_running_line(
            puter.line_number_to_run)

new_loop = None


def run_code_thread():
    global new_loop
    new_loop = asyncio.new_event_loop()
    # async def run_codes_async():
    load_input()
    for puter in computers:
        new_loop.create_task(run_puter_forever(computers[puter]))
    new_loop.run_forever()


def run_code():
    run_thread = threading.Thread(
        name="run codes", target=run_code_thread, args=(), daemon=True)
    run_thread.start()
    # while True:
    #     step_forward_code()


def pause_code():
    new_loop.stop()


def start_event_loop(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


threading.Thread(target=start_event_loop, args=(loop,), daemon=True).start()
with dpg.handler_registry():
    dpg.add_key_release_handler(
        key=dpg.mvKey_F11, callback=lambda: dpg.toggle_viewport_fullscreen())

# 创建窗口
with dpg.window(label="Control Panel", width=300, height=820, no_resize=True, autosize=False):
    dpg.add_text("Counter: 0", tag="counter_text")
    dpg.add_button(label="TOGGLE", callback=toggle_show)
    dpg.add_button(label="Step", callback=step_forward_code)
    dpg.add_button(label="Run", callback=run_code)
    dpg.add_button(label="Stop", callback=pause_code)
    dpg.add_button(label="Load", callback=load_input)
with dpg.window(tag="computers", pos=[300, 0], width=1100, height=820, no_resize=True, no_title_bar=True, autosize=False):
    for row in range(3):
        nodes.append([])
        with dpg.group(pos=[20, 40 + row * 250], horizontal=True, horizontal_spacing=54) as node_column:
            for col in range(4):
                node = Node(row, col)
                node.submit(node_column)
                nodes[row].append(node)

# ctypes.windll.shcore.SetProcessDpiAwareness(2)
dpg.create_viewport(title="TIS-100 Emulator", width=1400,
                    height=820, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.set_primary_window("primary_window", True)
# 启动Dear PyGui
dpg.start_dearpygui()
dpg.destroy_context()
