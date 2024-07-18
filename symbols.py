# len = 13
operate_list = [
    "mov",
    "add",
    "sub",
    "jgz",
    "jlz",
    "jez",
    "jnz",
    "jmp",
    "jro",
    "neg",
    "sav",
    "swp",
    "nop",
]
operate_num_list = [3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1]
regs_list = [
    "left",
    "right",
    "up",
    "down",
    "last",
    "any",
    "nil",
    "acc",
    "bak",
]


def is_literal(str: str):
    return str.isdigit()


def is_reg(str: str):
    return str in regs_list


def is_position_reg(posi_str: str):
    return posi_str in regs_list[:-2]


def is_position_source_reg(posi_str: str):
    return posi_str in regs_list[:-3]


def is_source_reg(reg_str: str):
    return reg_str in (regs_list[:6] + ["acc"])


def is_dest_reg(reg_str: str):
    return reg_str in regs_list[:8]


def is_operater(str: str):
    return str in operate_list


def is_no_parameter_op(str: str):
    return str in operate_list[-4:]


def is_jump_label_op(str: str):
    return str in ["jmp", "jez", "jgz", "jlz", "jnz"]
