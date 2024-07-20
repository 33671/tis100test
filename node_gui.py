import dearpygui.dearpygui as dpg


class Node:

    def __init__(self, row, col):
        self.run_tag = "running" + str(row) + str(col)
        self.edit_tag = "edit" + str(row) + str(col)
        self.is_running = False
        with dpg.stage() as self._staging_container_id:
            dpg.add_input_text(width=220, height=201,
                               multiline=True, uppercase=True, show=True, tag=self.edit_tag)
            with dpg.drawlist(width=220, height=201, show=False, tag=self.run_tag):
                dpg.draw_rectangle(pmin=[0, 0], pmax=[220, 201])
                for n in range(15):
                    dpg.draw_text(pos=[10, 13 * n], text="MOV ACC, DOWN",
                                  color=(row * 80, 255 - row * 80, 255 - row * 40), size=13)
                dpg.draw_rectangle(
                    pmin=[0, 13 * 3], pmax=[220, 13*4], fill=(255, 255, 255), tag=self.run_tag+"line", show=False)
                # dpg.draw_text(pos=[10,13 * 3],text=tag_s , color=(0,0,0),size=13,tag=tag_s)

    def set_running_line(self, line_num: int):
        dpg.configure_item(
            self.run_tag + "line", pmin=[0, 13 * line_num], pmax=[220, 13 * (line_num + 1)], show=True)

    def switch_edit(self):
        dpg.show_item(self.edit_tag)
        dpg.hide_item(self.run_tag)
    
    def switch_run(self):
        dpg.show_item(self.run_tag)
        dpg.hide_item(self.edit_tag)

    def submit(self, parent):
        dpg.push_container_stack(parent)
        dpg.unstage(self._staging_container_id)
        dpg.pop_container_stack()
