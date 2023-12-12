#!/usr/bin/env python

import re
from itertools import combinations


def variations(count: int, damaged: int):
    for positions in combinations(range(count), damaged):
        yield ["#" if i in positions else "." for i in range(count)]


def apply_variation(conditions, variation):
    for new_condition in variation:
        conditions = conditions.replace("?", new_condition, 1)
    return conditions


def grouping(conditions: str) -> list[int]:
    return [len(group) for group in re.findall("#+", conditions)]


def p1(data, is_sample):
    answer = 0
    for line in data:
        conditions, target_grouping = line.split()
        target_grouping = list(map(int, target_grouping.split(",")))

        unknowns = conditions.count("?")
        known_damaged = conditions.count("#")
        target_damaged = sum(target_grouping)
        for variation in variations(unknowns, target_damaged - known_damaged):
            variant_conditions = apply_variation(conditions, variation)
            if grouping(variant_conditions) == target_grouping:
                answer += 1

    return answer


def p2(data, is_sample):
    if not is_sample:
        return "N/A"
    return "N/A"

    # my naive, brute force implementation for p1 is not feasible with this
    # input...
