from typing import List
import dearpygui.dearpygui as dpg


class Node:

    def __init__(self, row, col):
        self.run_tag = "running" + str(row) + str(col)
        self.edit_tag = "edit" + str(row) + str(col)
        self.is_running = False
        self.X = col
        self.Y = row
        self.texts_container: List[str | int] = []
        dpg.draw_arrow(p1=[self.X * (220 + 45) + 20 + 110 + 7, self.Y * 250 + 30], p2=[
                       self.X * (220 + 45) + 20 + 110 + 7, self.Y * 250 - 15], parent="computers")
        dpg.draw_arrow(p1=[self.X * (220 + 45) + 20 + 110 + 7, 3 * 250 + 20], p2=[
                       self.X * (220 + 45) + 20 + 110 + 7, 3 * 250 - 15], parent="computers")
        if self.Y != 2:
            dpg.draw_arrow(p1=[self.X * (220 + 45) + 20 + 110 - 10 - 7, (self.Y + 1) * 203 + self.Y * 49 + 30], p2=[
                           self.X * (220 + 45) + 20 + 110 - 10 - 7, (self.Y + 1) * 250 + 30], parent="computers")
        if self.X != 0:
            dpg.draw_arrow(p1=[self.X * (220 + 54) + 10, self.Y * 250 + 120], p2=[
                           self.X * 220 + 12 + 54 * (self.X - 1), self.Y * 250 + 120], parent="computers")
        if self.X != 3:
            dpg.draw_arrow(p1=[(self.X + 1) * 220 + 12 + 54 * self.X, self.Y * 250 + 135], p2=[
                           (self.X + 1) * 220 + 54 * (self.X + 1)+12, self.Y * 250 + 135], parent="computers")
        # dpg.draw_arrow(p1=[20 + self.X * 220])
        with dpg.stage() as self._staging_container_id:
            dpg.add_input_text(width=220, height=201,
                               multiline=True, uppercase=True, show=True, tag=self.edit_tag)
            with dpg.drawlist(width=220, height=201, show=False, tag=self.run_tag):
                dpg.draw_rectangle(pmin=[0, 0], pmax=[220, 201])
                dpg.draw_rectangle(
                    pmin=[0, 13 * 3], pmax=[220, 13*4], fill=(255, 255, 255), tag=self.run_tag+"line", show=False)
                for n in range(15):
                    tag = dpg.draw_text(pos=[10, 13 * n], text="MOV ACC, DOWN",
                                        color=(col * 80, 255 - row * 80 + n * 5, 255 - row * 40), size=13)
                    self.texts_container.append(tag)
                # dpg.draw_text(pos=[10,13 * 3],text=tag_s , color=(0,0,0),size=13,tag=tag_s)

    def set_running_line(self, line_num: int):
        if line_num == -1:
            dpg.configure_item(
                self.run_tag + "line", show=False)
        dpg.configure_item(
            self.run_tag + "line", pmin=[0, 13 * line_num], pmax=[220, 13 * (line_num + 1)], show=True)

    def set_run_texts(self, texts: List[str]):
        for container_index, tag in enumerate(self.texts_container):
            if container_index < len(texts):
                dpg.configure_item(
                    tag, text=texts[container_index])
            else:
                dpg.configure_item(
                    tag, text="")

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
