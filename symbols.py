#len = 13
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
    for reg in regs_list:
        if reg == str:
            return True
    return False


def is_position_reg(posi_str: str):
    for reg in regs_list[:-2]:
        if reg == posi_str:
            return True
    return False


def is_source_reg(reg_str: str):
    for reg in regs_list[:4] + ["acc", "any"]:
        if reg == reg_str:
            return True
    return False


def is_dest_reg(reg_str: str):
    for reg in regs_list[:4] + ["acc", "nil"]:
        if reg == reg_str:
            return True
    return False


def is_operater(str: str):
    for operate in operate_list:
        if operate == str:
            return True
    return False


def is_no_parameter_op(str: str):
    for op in operate_list[-4:]:
        if op == str:
            return True
    return False


def is_jump_label_op(str: str):
    for op in ["jmp", "jez", "jgz", "jlz", "jnz"]:
        if op == str:
            return True
    return False