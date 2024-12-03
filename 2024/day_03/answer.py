#!/usr/bin/env python

import re
from functools import reduce

def p1(data: list[str], is_sample: bool):
    memory = ''.join(data)
    multiply_instruction = re.compile(r'mul\((?P<fac1>\d+),(?P<fac2>\d+)\)')

    total = 0
    for instruction in multiply_instruction.finditer(memory):
        total += reduce(lambda x, y: x*y, map(int, instruction.groups()))

    return total

def p2(data: list[str], is_sample: bool):
    memory_corrupt = ''.join(data).split('don\'t()')
    memory = memory_corrupt.pop(0)
    for mem in memory_corrupt:
        try:
            memory += mem.split('do()', 1)[1]
        except IndexError:
            pass

    multiply_instruction = re.compile(r'mul\((?P<fac1>\d+),(?P<fac2>\d+)\)')

    total = 0
    for instruction in multiply_instruction.finditer(memory):
        total += reduce(lambda x, y: x*y, map(int, instruction.groups()))

    return total
