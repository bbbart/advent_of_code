#!/usr/bin/env python

from collections import defaultdict
from functools import cache


def p1(data, is_sample):
    garden_plots = set()
    starting_pos = None
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                continue
            if char == "S":
                starting_pos = (x, y)
            garden_plots.add((x, y))

    garden = {}
    for co in garden_plots:
        neighbours = {
            (nx, ny)
            for nx, ny in (
                (co[0] - 1, co[1]),
                (co[0] + 1, co[1]),
                (co[0], co[1] - 1),
                (co[0], co[1] + 1),
            )
            if (nx, ny) in garden_plots
        }
        garden[co] = neighbours

    targets = {starting_pos}
    for _ in range(64):
        new_targets = set().union(*(garden[t] for t in targets))
        targets = new_targets

    return len(targets)


def p2(data, is_sample):
    # this works, in theory, but is too slow and takes up too much memory
    # so, in other words: it doesn't work :-)
    garden_plots = set()
    starting_pos = None
    x, y = 0, 0
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                continue
            if char == "S":
                starting_pos = (x, y)
            garden_plots.add((x, y))

    map_width = x + 1
    map_height = y + 1

    def show_field(locations):
        fieldcos = set().union(*locations.values())
        for field_y in range(
            min(fc[1] for fc in fieldcos), max(fc[1] for fc in fieldcos) + 1
        ):
            for y in range(map_height):
                for field_x in range(
                    min(fc[0] for fc in fieldcos),
                    max(fc[1] for fc in fieldcos) + 1,
                ):
                    for x in range(map_width):
                        if (field_x, field_y) in locations[(x, y)]:
                            char = "O"
                        elif (x, y) in garden_plots:
                            char = "."
                        else:
                            char = "#"
                        print(char, end="")
                print()
        print()

    @cache
    def get_open_directions(loc: tuple[int, int]) -> set[tuple[int, int]]:
        """All directions accessible from the given destinations."""
        return {
            (dx, dy)
            for dx, dy in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            )
            if ((loc[0] + dx) % map_width, (loc[1] + dy) % map_height)
            in garden_plots
        }

    @cache
    def neighbours(current_position):
        nbs = set()
        for direction in get_open_directions(current_position):
            localco = (
                current_position[0] + direction[0],
                current_position[1] + direction[1],
            )
            fieldco_delta = (0, 0)
            if localco[0] < 0:
                fieldco_delta = (-1, 0)
                localco = localco[0] % map_width, localco[1]
            elif localco[0] >= map_width:
                fieldco_delta = (1, 0)
                localco = localco[0] % map_width, localco[1]
            elif localco[1] < 0:
                fieldco_delta = (0, -1)
                localco = localco[0], localco[1] % map_height
            elif localco[1] >= map_height:
                fieldco_delta = (0, 1)
                localco = localco[0], localco[1] % map_height

            if localco in garden_plots:
                nbs.add((localco, fieldco_delta))

        return nbs

    total_steps = 26501365
    destinations = {0: defaultdict(set), 1: defaultdict(set)}
    destinations[0][starting_pos].add((0, 0))
    for step in range(1, total_steps + 1):
        for loc, fields in destinations[(step - 1) % 2].items():
            if not destinations[(step - 1) % 2][loc]:
                continue
            for newlocal, fielddelta in neighbours(loc):
                destinations[step % 2][newlocal] |= {
                    (field[0] + fielddelta[0], field[1] + fielddelta[1])
                    for field in fields
                }

    return sum(
        len(fields) for loc, fields in destinations[total_steps % 2].items()
    )
