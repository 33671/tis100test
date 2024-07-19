from typing import List, Dict
from symbols import is_literal, is_position_source_reg
from channel import DataChannel
import asyncio
from instruction import Instruction
from syntax import gen_syntax
from grid import channels


class Computer:
    def __init__(self, x: int, y: int, program: str | None = None) -> None:
        self.X: int = x
        self.Y: int = y
        self.lines: List[List[str]] = []
        self.line_number_to_run: int = 0
        self.instructions: List[Instruction] = []
        self.labels_index: Dict[str, int] = {}
        self.is_waiting_for_input: bool = False
        self.is_waiting_for_output: bool = False
        self.ACC: int = 0
        self.BAK: int = 0
        self.LAST: str = "up"
        if program is None:
            return
        file_lines = program.splitlines()
        for line in file_lines:
            line_trimed = line.strip().lower().replace(",", " ")
            if line_trimed.startswith("#") or line_trimed == "":
                self.lines.append(["nop"])
                continue
            if line_trimed.find(":") != -1:
                label_and_code = [x.strip()
                                  for x in line_trimed.split(":")]
                if len(label_and_code) != 2 or len(label_and_code[0]) == 0:
                    raise Exception("bad lable syntax")
                if label_and_code[1].strip() == "":  # bare lable
                    self.labels_index[label_and_code[0].strip()] = len(
                        self.lines)
                    self.lines.append(["nop"])
                    continue
                else:  # lable and code
                    self.labels_index[label_and_code[0].strip()] = len(
                        self.lines)
                    self.lines.append([i for i in label_and_code[1].split(
                        " ") if i != "" and i != " "])
                    continue
            line_elements = [i for i in line_trimed.split(
                " ") if i != "" and i != " "]
            self.lines.append(line_elements)
        print("labels:", self.labels_index)
        inses = gen_syntax(self.lines, self.labels_index)
        if type(inses) == bool:
            raise Exception("!syntax error")
        else:
            self.instructions = inses
            print(self.instructions)

    async def block_waiting_for_data_from(self, data_source: str) -> int:
        print(f"<-- {self.X}${self.Y} waiting read from {data_source}")
        self.is_waiting_for_input = True
        if data_source == 'any':
            tasks = {}
            for direction in ["up", "down", "left", "right"]:
                direct_task = asyncio.create_task(
                    self.get_read_neighbor_channel(direction).read())
                tasks[direct_task] = direction
            done, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            for task in done:
                last = tasks[task]
                self.LAST = last
                read_data = task.result()
                print(
                    f"<-- {self.X}${self.Y} data read from any:{last} = {read_data}")
                self.is_waiting_for_input = False
                return read_data
            return
        if data_source == 'last':
            chan = self.get_read_neighbor_channel(self.LAST)
            read_data = await chan.read()
            self.is_waiting_for_input = False
            return read_data
        chan = self.get_read_neighbor_channel(data_source)
        item = await chan.read()
        print(f"<-- {self.X}${self.Y} data read: {data_source} = {item}")
        self.is_waiting_for_input = False
        return item

    async def block_waiting_send(self, data: int, dest_position: str):
        print(f"--> {self.X}${self.Y} sending {data} {dest_position}")
        self.is_waiting_for_output = True
        if dest_position == "any":
            tasks = {}
            for direction in ["up", "down", "left", "right"]:
                direct_task = asyncio.create_task(
                    self.get_write_neighbor_channel(direction).send(data))
                tasks[direct_task] = direction
            done, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            for task in done:
                last = tasks[task]
                self.LAST = last
                break
            self.is_waiting_for_output = False
            return
        if dest_position == "last":
            chan = self.get_write_neighbor_channel(self.LAST)
            await chan.send(data)
            self.is_waiting_for_output = False
            return
        if dest_position == "nil":
            return
        chan = self.get_write_neighbor_channel(dest_position)
        await chan.send(data)
        self.is_waiting_for_output = False
        print(f"--> {self.X}${self.Y} data {data} sent {dest_position}")

    def get_write_neighbor_channel_posi(self, position: str) -> str:
        dict_key = ""
        if position == "up":
            dict_key = f"X1:{self.X} Y1:{self.Y} X2:{self.X} Y2:{self.Y - 1}"
        if position == "down":
            dict_key = f"X1:{self.X} Y1:{self.Y} X2:{self.X} Y2:{self.Y + 1}"
        if position == "left":
            dict_key = f"X1:{self.X} Y1:{self.Y} X2:{self.X - 1} Y2:{self.Y}"
        if position == "right":
            dict_key = f"X1:{self.X} Y1:{self.Y} X2:{self.X + 1} Y2:{self.Y}"
        # print(f"{self.X}${self.Y} writing: try find existing:", dict_key)
        return dict_key

    def get_read_neighbor_channel_posi(self, position: str) -> str:
        dict_key = ""
        if position == "up":
            dict_key = f"X1:{self.X} Y1:{self.Y - 1} X2:{self.X} Y2:{self.Y}"
        if position == "down":
            dict_key = f"X1:{self.X} Y1:{self.Y + 1} X2:{self.X} Y2:{self.Y}"
        if position == "left":
            dict_key = f"X1:{self.X - 1} Y1:{self.Y} X2:{self.X} Y2:{self.Y}"
        if position == "right":
            dict_key = f"X1:{self.X + 1} Y1:{self.Y} X2:{self.X} Y2:{self.Y}"
        # print(f"{self.X}${self.Y} reading: try find existing:", dict_key)
        return dict_key

    def get_write_neighbor_channel(self, position: str) -> DataChannel:
        posi = self.get_write_neighbor_channel_posi(position)
        if posi not in channels:
            channels[posi] = DataChannel()
        return channels[posi]

    def get_read_neighbor_channel(self, position: str) -> DataChannel:
        posi = self.get_read_neighbor_channel_posi(position)
        if posi not in channels:
            channels[posi] = DataChannel()
        return channels[posi]

    def pc_increment(self, index: int) -> int:
        length = len(self.instructions)
        index += 1
        if index >= length:
            index = 0
        return index

    async def excute_line(self, index: int) -> int:
        if len(self.instructions) == 0 or len(self.instructions) <= index:
            await asyncio.Future()
        ins = self.instructions[index]
        print(f"{self.X}${self.Y} current:", ins)
        if ins.Op == "mov":
            if ins.Dest == "acc":
                if is_literal(ins.Src):
                    self.ACC = int(ins.Src)
                elif ins.Src == "acc":
                    pass
                elif is_position_source_reg(ins.Src):
                    data_rec = await self.block_waiting_for_data_from(ins.Src)
                    self.ACC = data_rec
                else:
                    raise Exception("undefined behavior")
            else:
                if is_literal(ins.Src):
                    await self.block_waiting_send(int(ins.Src), ins.Dest)
                elif is_position_source_reg(ins.Src):
                    data_rec = await self.block_waiting_for_data_from(ins.Src)
                    await self.block_waiting_send(data_rec, ins.Dest)
                elif ins.Src == "acc":
                    await self.block_waiting_send(self.ACC, ins.Dest)
                else:
                    raise Exception("undefined behavior")
            return self.pc_increment(ins.LineIndex)
        elif ins.Op == "add":
            if type(ins.Src) == int:
                self.ACC += ins.Src
            elif ins.Src == "acc":
                self.ACC *= 2
            elif is_position_source_reg(ins.Src):
                data_rec = await self.block_waiting_for_data_from(ins.Src)
                self.ACC += data_rec
            else:
                raise Exception("undefined behavior")
            return self.pc_increment(ins.LineIndex)
        elif ins.Op == "sub":
            if type(ins.Src) == int:
                self.ACC -= ins.Src
            elif ins.Src == "acc":
                self.ACC = 0
            elif is_position_source_reg(ins.Src):
                data_rec = await self.block_waiting_for_data_from(ins.Src)
                self.ACC -= data_rec
            else:
                raise Exception("undefined behavior")
            return self.pc_increment(ins.LineIndex)
        elif ins.Op == "jgz":
            if self.ACC > 0:
                return self.labels_index[ins.Label]
            else:
                return self.pc_increment(ins.LineIndex)
        elif ins.Op == "jlz":
            if self.ACC < 0:
                return self.labels_index[ins.Label]
            else:
                return self.pc_increment(ins.LineIndex)
        elif ins.Op == "jez":
            if self.ACC == 0:
                return self.labels_index[ins.Label]
            else:
                return self.pc_increment(ins.LineIndex)
        elif ins.Op == "jnz":
            if self.ACC != 0:
                return self.labels_index[ins.Label]
            else:
                return self.pc_increment(ins.LineIndex)
        elif ins.Op == "jmp":
            return self.labels_index[ins.Label]
        elif ins.Op == "jro":
            offset = 0
            if is_literal(ins.Src):
                offset = int(ins.Src)
                if offset == 0:
                    # program halt
                    await asyncio.Future()
            elif ins.Src == "acc":
                offset = self.ACC
            else:
                offset = await self.block_waiting_for_data_from(ins.Src)
            jump_dest = ins.LineIndex + offset
            if jump_dest < 0 or jump_dest >= len(self.instructions):
                jump_dest = 0
            return jump_dest
        elif ins.Op == "neg":
            self.ACC = -self.ACC
            return self.pc_increment(ins.LineIndex)
        elif ins.Op == "swp":
            temp = self.ACC
            self.ACC = self.BAK
            self.BAK = temp
            return self.pc_increment(ins.LineIndex)
        elif ins.Op == "sav":
            self.BAK = self.ACC
            return self.pc_increment(ins.LineIndex)
        elif ins.Op == "nop":
            return self.pc_increment(ins.LineIndex)

    async def excute_next(self):
        self.line_number_to_run = await self.excute_line(self.line_number_to_run)
        return self
