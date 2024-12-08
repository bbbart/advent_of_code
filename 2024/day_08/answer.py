#!/usr/bin/env python

from collections import defaultdict
from itertools import combinations


def p1(data: list[str], is_sample: bool):
    antennas: dict[chr, list[tuple[int]]] = defaultdict(list)
    x, y = 0, 0
    for line in data:
        x = 0
        for char in line:
            if char != ".":
                antennas[char].append((x, y))
            x += 1
        y += 1

    width = x
    height = y

    antinodes = set()
    for _, locs in antennas.items():
        for pair in combinations(locs, 2):
            delta = abs(pair[0][0] - pair[1][0]), abs(pair[0][1] - pair[1][1])

            if pair[0][0] < pair[1][0]:
                antinodes_x = (pair[0][0] - delta[0], pair[1][0] + delta[0])
            else:
                antinodes_x = (pair[0][0] + delta[0], pair[1][0] - delta[0])

            if pair[0][1] < pair[1][1]:
                antinodes_y = (pair[0][1] - delta[1], pair[1][1] + delta[1])
            else:
                antinodes_y = (pair[0][1] + delta[1], pair[1][1] - delta[1])

            for antinode in zip(antinodes_x, antinodes_y):
                if 0 <= antinode[0] < width and 0 <= antinode[1] < height:
                    antinodes.add(antinode)

    return len(antinodes)


def p2(data: list[str], is_sample: bool):
    antennas: dict[chr, list[tuple[int]]] = defaultdict(list)
    x, y = 0, 0
    for line in data:
        x = 0
        for char in line:
            if char != ".":
                antennas[char].append((x, y))
            x += 1
        y += 1

    width = x
    height = y

    antinodes = set()
    for _, locs in antennas.items():

        # non-unique frequency antennas are also antinodes themselves
        if len(locs) > 1:
            antinodes.update(locs)

        for pair in combinations(locs, 2):
            delta = abs(pair[0][0] - pair[1][0]), abs(pair[0][1] - pair[1][1])

            if pair[0][0] < pair[1][0]:  # first pair member is leftmost
                if pair[0][1] < pair[1][1]:  # first pair member is topmost
                    antinodes.update(
                        zip(
                            range(pair[0][0], -1, -delta[0]),
                            range(pair[0][1], -1, -delta[1]),
                        )
                    )
                    antinodes.update(
                        zip(
                            range(pair[1][0], width, delta[0]),
                            range(pair[1][1], height, delta[1]),
                        )
                    )
                else:  # first pair member is bottommost
                    antinodes.update(
                        zip(
                            range(pair[0][0], -1, -delta[0]),
                            range(pair[0][1], height, delta[1]),
                        )
                    )
                    antinodes.update(
                        zip(
                            range(pair[1][0], width, delta[0]),
                            range(pair[1][1], -1, -delta[1]),
                        )
                    )
            else:  # first pair member is rightmost
                if pair[0][1] < pair[1][1]:  # first pair member is topmost
                    antinodes.update(
                        zip(
                            range(pair[0][0], width, delta[0]),
                            range(pair[0][1], -1, -delta[1]),
                        )
                    )
                    antinodes.update(
                        zip(
                            range(pair[1][0], -1, -delta[0]),
                            range(pair[1][1], height, delta[1]),
                        )
                    )
                else:  # first pair member is bottommost
                    antinodes.update(
                        zip(
                            range(pair[0][0], width, delta[0]),
                            range(pair[0][1], height, delta[1]),
                        )
                    )
                    antinodes.update(
                        zip(
                            range(pair[1][0], -1, -delta[0]),
                            range(pair[1][1], -1, -delta[1]),
                        )
                    )

    return len(antinodes)
