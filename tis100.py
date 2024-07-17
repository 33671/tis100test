from typing import List, Dict
import time
from symbols import is_dest_reg, is_jump_label_op, is_literal, is_operater, is_source_reg, is_no_parameter_op


class Instruction:
    Op: str
    Src: str | int
    Dest: str
    LineIndex: int
    Label: str

    def __init__(self, op, line_index, src="", dest="", label="") -> None:
        self.Op = op
        self.Src = src
        self.Dest = dest
        self.LineIndex = line_index
        self.Label = label

    def __repr__(self) -> str:
        return f"\n[\t{self.Op} \t{self.Src}\t {self.Dest}\tIndex={self.LineIndex}]"

    def __str__(self) -> str:
        return f"{self.Op} {self.Src} {self.Dest}\tIndex={self.LineIndex}"


class Computer:
    ACC: int = 0
    BAK: int = 0
    line_number_to_run: int = 0
    is_waiting_for_input: bool = False
    is_waiting_for_output: bool = False
    lines: List[List[str]] = []
    instructions: List[Instruction] = None
    labels_index: Dict[str, int] = {}

    def __init__(self, program_file: str) -> None:
        with open(program_file, "r") as f:
            file_lines = f.readlines()
            for line in file_lines:
                line_trimed = line.strip().lower().replace(",", " ")
                if line_trimed.startswith("#"):
                    continue
                if line_trimed.find(":") != -1:
                    label_and_code = [x.strip()
                                      for x in line_trimed.split(":")]
                    if len(label_and_code) != 2 or len(label_and_code[0]) == 0:
                        raise Exception("bad lable syntax")
                    if label_and_code[1].strip() == "":  # bare lable
                        self.labels_index[label_and_code[0].strip()] = len(
                            self.lines)
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
        print("labels:",self.labels_index)

    async def block_waiting_for_data(self, data_source: str) -> int:
        return 1

    def natural_increment(self, index: int) -> int:
        length = len(self.instructions)
        index += 1
        if index >= length:
            index = 0
        return index

    def gen_syntax(self) -> bool:
        self.instructions = []
        for line_index, line in enumerate(self.lines):
            if not is_operater(line[0]):
                print("invaild operater found:", line[0])
                return False
            if len(line) == 3:  # mov
                if line[0] != 'mov':
                    print("invaild 3 parameters:", line)
                    return False
                if not (is_source_reg(line[1]) or is_literal(line[1])):
                    print("invaild mov source found")
                    return False
                if not is_dest_reg(line[2]):
                    print("invaild mov dest found")
                    return False
                self.instructions.append(Instruction(
                    op="mov", line_index=line_index, src=line[1], dest=line[2]))
            elif len(line) == 2:  # jmp jez jgz jlz jnz
                if is_jump_label_op(line[0]):
                    if line[1] not in self.labels_index:
                        print("jump label not found")
                        return False
                    self.instructions.append(Instruction(
                        op=line[0], line_index=line_index, label=line[1]))
                elif line[0] == 'jro':  # jro
                    if not (is_literal(line[1]) or line[1] == "acc"):
                        print("invalid jro source")
                        return False
                    self.instructions.append(Instruction(
                        op="jro", line_index=line_index, src=line[1]))
                elif line[0] == 'add' or line[0] == "sub":  # add sub
                    if is_literal(line[1]):
                        self.instructions.append(Instruction(
                            op=line[0], line_index=line_index, src=int(line[1])))
                        continue
                    elif is_source_reg(line[1]):
                        self.instructions.append(Instruction(
                            op=line[0], line_index=line_index, src=line[1]))
                        continue
                    print("invalid add or sub source")
                    return False
                else:
                    print("invalid 2 parameters:", line)
                    return False
            # neg sav swp nop
            elif len(line) == 1:
                if not is_no_parameter_op(line[0]):
                    print("redundant 1 op parameter")
                    return False
                self.instructions.append(Instruction(
                    op=line[0], line_index=line_index))
            else:
                print("invalid parameters:", line)
                return False
        return True

    def excute_line(self, index: int) -> int:
        if self.instructions == None:
            if not self.gen_syntax():
                raise Exception("syntax error")
            print(self.instructions)
        ins = self.instructions[index]
        print("current:", ins)
        if ins.Op == "mov":
            if ins.Dest == "acc":
                if is_literal(ins.Src):
                    self.ACC = int(ins.Src)
                else:
                    raise NotImplementedError()
            else:
                raise NotImplementedError()
            return self.natural_increment(ins.LineIndex)
        elif ins.Op == "add":
            if type(ins.Src) == int:
                self.ACC += ins.Src
            elif ins.Src == "acc":
                self.ACC *= 2
            else:
                raise NotImplementedError()
            return self.natural_increment(ins.LineIndex)
        elif ins.Op == "sub":
            if type(ins.Src) == int:
                self.ACC -= ins.Src
            elif ins.Src == "acc":
                self.ACC = 0
            else:
                raise NotImplementedError()
            return self.natural_increment(ins.LineIndex)
        elif ins.Op == "jgz":
            if self.ACC > 0:
                return self.labels_index[ins.Label]
            else:
                return self.natural_increment(ins.LineIndex)
        elif ins.Op == "jlz":
            if self.ACC < 0:
                return self.labels_index[ins.Label]
            else:
                return self.natural_increment(ins.LineIndex)
        elif ins.Op == "jez":
            if self.ACC == 0:
                return self.labels_index[ins.Label]
            else:
                return self.natural_increment(ins.LineIndex)
        elif ins.Op == "jnz":
            if self.ACC != 0:
                return self.labels_index[ins.Label]
            else:
                return self.natural_increment(ins.LineIndex)
        elif ins.Op == "jmp":
            return self.labels_index[ins.Label]
        elif ins.Op == "jro":
            offset = 0
            if is_literal(ins.Src):
                offset = int(ins.Src)
            else:
                offset = self.ACC
            jump_dest = ins.LineIndex + offset
            if jump_dest < 0 or jump_dest >= len(self.instructions):
                jump_dest = 0
            return jump_dest
        elif ins.Op == "neg":
            self.ACC = -self.ACC
            return self.natural_increment(ins.LineIndex)
        elif ins.Op == "swp":
            temp = self.ACC
            self.ACC = self.BAK
            self.BAK = temp
            return self.natural_increment(ins.LineIndex)
        elif ins.Op == "sav":
            self.BAK = self.ACC
            return self.natural_increment(ins.LineIndex)
        elif ins.Op == "nop":
            return self.natural_increment(ins.LineIndex)

    def excute_next(self):
        self.line_number_to_run = self.excute_line(self.line_number_to_run)
        return self


com = Computer("tis100.txt")
while True:
    time.sleep(1)
    com.excute_next()
    print("acc", com.ACC)
