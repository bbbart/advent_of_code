def run_program(program: list[str], registers: dict[str, int]):
    instr_ptr = 0
    while True:
        try:
            instr = program[instr_ptr].split()
        except IndexError:
            break

        if instr[0] == "cpy":
            try:
                registers[instr[2]] = int(instr[1])
            except ValueError:
                registers[instr[2]] = registers[instr[1]]
        elif instr[0] == "inc":
            registers[instr[1]] += 1
        elif instr[0] == "dec":
            registers[instr[1]] -= 1
        elif instr[0] == "jnz":
            try:
                if registers[instr[1]] != 0:
                    instr_ptr += int(instr[2]) - 1
            except KeyError:
                if instr[1] != 0:
                    instr_ptr += int(instr[2]) - 1
        instr_ptr += 1


def p1(data, is_sample):
    registers: dict[str, int] = dict(a=0, b=0, c=0, d=0)
    instructions = list(data)

    run_program(instructions, registers)

    return registers["a"]


def p2(data, is_sample):
    registers: dict[str, int] = dict(a=0, b=0, c=1, d=0)
    instructions = list(data)

    run_program(instructions, registers)

    return registers["a"]
