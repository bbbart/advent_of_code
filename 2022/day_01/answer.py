#!/usr/bin/env python

from collections import defaultdict


def parse_input(data):
    cals_per_elf = defaultdict(int)
    elfindex = 0
    for cals in data:
        if cals == "":
            elfindex += 1
            continue
        cals_per_elf[elfindex] += int(cals.strip())
    return cals_per_elf


def p1(data):
    cals_per_elf = parse_input(data)
    return max(cals_per_elf.values())


def p2(data):
    cals_per_elf = parse_input(data)
    return sum(sorted(cals_per_elf.values())[-3:])
