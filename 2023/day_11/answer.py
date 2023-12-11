#!/usr/bin/env python

from itertools import combinations


def calculate_distance(data, expansion_rate=1):
    galaxies = set()
    x, y = 0, 0
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.add((x, y))

    emptycols = set(
        col for col in range(x) if col not in [gal[0] for gal in galaxies]
    )
    emptyrows = set(
        row for row in range(y) if row not in [gal[1] for gal in galaxies]
    )

    distance_sum = 0
    for gal1, gal2 in combinations(galaxies, 2):
        normal_distance = abs(gal1[0] - gal2[0]) + abs(gal1[1] - gal2[1])
        expanded_cols = len(
            emptycols
            & set(range(min(gal1[0], gal2[0]) + 1, max(gal1[0], gal2[0])))
        )
        expanded_rows = len(
            emptyrows
            & set(range(min(gal1[1], gal2[1]) + 1, max(gal1[1], gal2[1])))
        )
        distance_sum += normal_distance + (expanded_cols + expanded_rows) * (
            expansion_rate - 1
        )

    return distance_sum


def p1(data, is_sample):
    return calculate_distance(data, 2)


def p2(data, is_sample):
    return calculate_distance(data, 1_000_000)
