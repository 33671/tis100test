from symbols import is_dest_reg, is_jump_label_op, is_literal, is_operater, is_source_reg, is_no_parameter_op, is_position_source_reg
from instruction import Instruction
from typing import List, Dict


def gen_syntax(lines: List[List[str]], labels_index: Dict[str, int]) -> bool | List[Instruction]:
    instructions: List[Instruction] = []
    for line_index, line in enumerate(lines):
        if not is_operater(line[0]):
            print("invaild operater found:", line)
            return False
        if len(line) == 3:  # mov
            if line[0] != 'mov':
                print("invaild 3 parameters:", line)
                return False
            if not (is_source_reg(line[1]) or is_literal(line[1])):
                print("invaild mov source found:", line)
                return False
            if not is_dest_reg(line[2]):
                print("invaild mov dest found:", line)
                return False
            instructions.append(Instruction(
                op="mov", line_index=line_index, src=line[1], dest=line[2]))
        elif len(line) == 2:  # jmp jez jgz jlz jnz
            if is_jump_label_op(line[0]):
                if line[1] not in labels_index:
                    print("jump label not found:", line)
                    return False
                instructions.append(Instruction(
                    op=line[0], line_index=line_index, label=line[1]))
            elif line[0] == 'jro':  # jro
                if not (is_literal(line[1]) or is_position_source_reg(line[1])):
                    print("invalid jro source", line)
                    return False
                instructions.append(Instruction(
                    op="jro", line_index=line_index, src=line[1]))
            elif line[0] == 'add' or line[0] == "sub":  # add sub
                if is_literal(line[1]):
                    instructions.append(Instruction(
                        op=line[0], line_index=line_index, src=int(line[1])))
                    continue
                elif is_source_reg(line[1]):
                    instructions.append(Instruction(
                        op=line[0], line_index=line_index, src=line[1]))
                    continue
                print("invalid add or sub source", line)
                return False
            else:
                print("invalid 2 parameters:", line)
                return False
        # neg sav swp nop
        elif len(line) == 1:
            if not is_no_parameter_op(line[0]):
                print("redundant 1 op parameter:", line)
                return False
            instructions.append(Instruction(
                op=line[0], line_index=line_index))
        else:
            print("invalid parameters:", line)
            return False
    return instructions
