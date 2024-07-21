import dearpygui.dearpygui as dpg
from node_gui import Node
dpg.create_context()
# 定义按钮回调函数


def increment_counter(sender, app_data, user_data):
    # 获取当前计数值
    current_value = dpg.get_value("counter_value")
    # 增加计数值
    new_value = current_value + 1
    # 更新计数值
    dpg.set_value("counter_value", new_value)
    # 更新显示的文本
    dpg.set_value("counter_text", f"Counter: {new_value}")


# 创建值注册表
with dpg.value_registry():
    # 创建一个初始值为0的整型值
    dpg.add_int_value(default_value=0, tag="counter_value")
    dpg.add_string_value(default_value="Default string", tag="string_value")
with dpg.handler_registry():
    dpg.add_key_release_handler(
        key=dpg.mvKey_F11, callback=lambda: dpg.toggle_viewport_fullscreen())

# 创建窗口
with dpg.window(label="Control Panel", width=300, height=820, no_resize=True, no_title_bar=True, no_move=True):
    dpg.add_text("Counter: 0", tag="counter_text")
    dpg.add_button(label="Increment", callback=increment_counter)
with dpg.window(tag="computers", pos=[300, 0], min_size=[1100, 820], no_resize=True, no_title_bar=True, no_move=True):
    for row in range(3):
        with dpg.group(pos=[20, 40 + row * 250], horizontal=True, horizontal_spacing=54) as node_column:
            for col in range(4):
                node = Node(row, col)
                node.submit(node_column)
                node.switch_run()
                node.set_run_texts(["HELLO","WORLD"])
                node.set_running_line(1)


dpg.create_viewport(title="TIS-100 Emulator", min_width=1400, min_height=820)
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.set_primary_window("primary_window", True)
# 启动Dear PyGui
dpg.start_dearpygui()
dpg.destroy_context()
