#!/usr/bin/env python

from itertools import product, combinations

def p1(data: list[str], is_sample: bool):
    entries = set(map(int, data))

    for a, b in product(entries, entries):
        if a == b:
            continue
        if a + b == 2020:
            return str(a * b)

def p2(data: list[str], is_sample: bool):
    entries = set(map(int, data))

    for a, b, c in combinations(entries, 3):
        if a + b + c == 2020:
            return str(a * b * c)
