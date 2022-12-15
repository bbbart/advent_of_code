#!/usr/bin/env python


def parse_data(data):
    for pairs in data:
        elf1, elf2 = pairs.split(",")
        spaces1_1, spaces1_2 = elf1.split("-")
        spaces2_1, spaces2_2 = elf2.split("-")
        space1 = set(range(int(spaces1_1), int(spaces1_2) + 1))
        space2 = set(range(int(spaces2_1), int(spaces2_2) + 1))
        yield space1, space2


def p1(data, is_sample):
    containscounter = 0
    for space1, space2 in parse_data(data):
        if space1.issubset(space2) or space2.issubset(space1):
            containscounter += 1

    return containscounter


def p2(data, is_sample):
    overlapcounter = 0
    for space1, space2 in parse_data(data):
        if space1.intersection(space2):
            overlapcounter += 1

    return overlapcounter
