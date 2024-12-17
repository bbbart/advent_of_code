#!/usr/bin/env python

import re


def run_program(program, registers):
    def combo(operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return registers["A"]
            case 5:
                return registers["B"]
            case 6:
                return registers["C"]
            case 7:
                raise NotImplementedError

    pointer = 0
    buffer = []
    while pointer < len(program):
        opcode = program[pointer]
        try:
            operand = program[pointer + 1]
        except IndexError:
            operand = None

        match opcode:
            case 0:  # adv
                registers["A"] = int(registers["A"] / 2 ** combo(operand))
                pointer += 2
            case 1:  # bxl
                registers["B"] ^= operand
                pointer += 2
            case 2:  # bst
                registers["B"] = combo(operand) % 8
                pointer += 2
            case 3:  # jnz
                if registers["A"] != 0:
                    pointer = operand
                else:
                    pointer += 2
            case 4:  # bxc
                registers["B"] = registers["B"] ^ registers["C"]
                pointer += 2
            case 5:  # out
                buffer.append(combo(operand) % 8)
                pointer += 2
            case 6:  # bdv
                registers["B"] = int(registers["A"] / 2 ** combo(operand))
                pointer += 2
            case 7:  # cdv
                registers["C"] = int(registers["A"] / 2 ** combo(operand))
                pointer += 2

    return buffer


def p1(data: list[str], is_sample: bool):
    registers = {}
    program = []
    for line in data:
        m = re.match(r"Register A: (\d+)", line)
        if m:
            registers["A"] = int(m.group(1))
            continue

        m = re.match(r"Register B: (\d+)", line)
        if m:
            registers["B"] = int(m.group(1))
            continue

        m = re.match(r"Register C: (\d+)", line)
        if m:
            registers["C"] = int(m.group(1))
            continue

        m = re.match(r"Program: ((\d,?)+)", line)
        if m:
            program = [int(x) for x in m.group(1).split(",")]
            continue

    return ",".join(str(x) for x in run_program(program, registers))


def p2(data: list[str], is_sample: bool):
    if is_sample:
        return "N/A"

    registers = {}
    program = []
    for line in data:
        m = re.match(r"Register A: (\d+)", line)
        if m:
            registers["A"] = int(m.group(1))
            continue

        m = re.match(r"Register B: (\d+)", line)
        if m:
            registers["B"] = int(m.group(1))
            continue

        m = re.match(r"Register C: (\d+)", line)
        if m:
            registers["C"] = int(m.group(1))
            continue

        m = re.match(r"Program: ((\d,?)+)", line)
        if m:
            program = [int(x) for x in m.group(1).split(",")]
            continue

    A = 0
    while True:
        registers["A"] = A
        output = run_program(program, registers)

        if len(output) < len(program):
            A = A * 7 + 1
            continue
        if len(output) > len(program):
            A = A // 8 - 1
            continue

        for i in range(len(program) - 1, -1, -1):
            if output[i] != program[i]:
                A += 8 ** (max(i - 1, 0))
                break
        else:
            return A
