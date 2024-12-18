#!/usr/bin/env python

import re

DELTAS = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}
DIRS = list(DELTAS)


def p1(data: list[str], is_sample: bool):
    grid: list[list[chr]] = []
    guard_pos = None, None
    guard_dir = None
    line, y = "", 0
    for line in data:
        grid.append(list(line))
        if match := re.search(r"\^|>|v|<", line):
            guard_dir = match.group()
            guard_pos = match.span()[0], y
        y += 1

    width = len(line)
    height = y

    guard_passed: set[tuple[int]] = set()
    guard_passed.add(guard_pos)

    while True:
        new_pos = (
            guard_pos[0] + DELTAS[guard_dir][0],
            guard_pos[1] + DELTAS[guard_dir][1],
        )

        if -1 in new_pos or new_pos[0] >= width or new_pos[1] >= height:
            break

        if grid[new_pos[1]][new_pos[0]] == "#":
            guard_dir = DIRS[(DIRS.index(guard_dir) + 1) % len(DIRS)]
        else:
            guard_pos = new_pos
            guard_passed.add(guard_pos)

    return len(guard_passed)


def p2(data: list[str], is_sample: bool):
    return 'N/A'

    # OPTION ONE (FAILS, finds too few)
    #  we determine if we are at a position where we can make a loop by
    #  imagining we *have to* turn right and then verify if that would
    #  bring us back to a previous position (and direction)
    #
    # grid: list[list[chr]] = []
    # guard_pos = None, None
    # guard_dir = None
    # line, y = "", 0
    # for line in data:
    #     grid.append(list(line))
    #     if match := re.search(r"\^|>|v|<", line):
    #         guard_dir = match.group()
    #         guard_pos = match.span()[0], y
    #     y += 1

    # width = len(line)
    # height = y

    # guard_passed: set[tuple[chr, tuple[int]]] = set()
    # guard_passed.add((guard_dir, guard_pos))

    # loop_blocks = set()
    # while True:
    #     imagined_dir = DIRS[(DIRS.index(guard_dir) + 1) % len(DIRS)]
    #     imagined_pos = guard_pos
    #     while True:
    #         if (imagined_dir, imagined_pos) in guard_passed:
    #             loop_blocks.add(
    #                 (
    #                     guard_pos[0] + DELTAS[guard_dir][0],
    #                     guard_pos[1] + DELTAS[guard_dir][1],
    #                 )
    #             )
    #             break
    #         imagined_pos = (
    #             imagined_pos[0] + DELTAS[imagined_dir][0],
    #             imagined_pos[1] + DELTAS[imagined_dir][1],
    #         )
    #         if (
    #             -1 in imagined_pos
    #             or imagined_pos[0] >= width
    #             or imagined_pos[1] >= height
    #             or grid[imagined_pos[1]][imagined_pos[0]] == "#"
    #         ):
    #             break

    #     # now stop imagining, and walk for real
    #     new_pos = (
    #         guard_pos[0] + DELTAS[guard_dir][0],
    #         guard_pos[1] + DELTAS[guard_dir][1],
    #     )

    #     if -1 in new_pos or new_pos[0] >= width or new_pos[1] >= height:
    #         break

    #     if grid[new_pos[1]][new_pos[0]] == "#":
    #         guard_dir = DIRS[(DIRS.index(guard_dir) + 1) % len(DIRS)]
    #     else:
    #         guard_pos = new_pos
    #         guard_passed.add((guard_dir, guard_pos))

    # return len(loop_blocks)

    # OPTION TWO (FAILS, finds too many)
    # obstacles_x: dict[int, list[int]] = defaultdict(list)
    # obstacles_y: dict[int, list[int]] = {}

    # y = 0
    # line = ''
    # for line in data:
    #     x_s = [m.span()[0] for m in re.finditer("#", line)]
    #     for x in x_s:
    #         obstacles_x[x].append(y)
    #     obstacles_y[y] = x_s
    #     y += 1

    # width = len(line)
    # height = y

    # loop_blocks = set()
    # for y1 in range(height - 1):
    #     for x1 in obstacles_y[y1]:
    #         y2 = y1 + 1
    #         for x2 in obstacles_y[y2]:
    #             if x2 <= x1:
    #                 continue
    #             for y3 in range(y2 + 1, height):
    #                 if x1 - 1 in obstacles_y[y3]:
    #                     loop_blocks.add((x2 - 1, y3 + 1))
    #                 elif x2 - 1 in obstacles_y[y3]:
    #                     loop_blocks.add((x1 - 1, y3 - 1))

    # for x1 in range(width - 1):
    #     for y1 in obstacles_x[x1]:
    #         x2 = x1 + 1
    #         for y2 in obstacles_x[x2]:
    #             if y2 >= y1:
    #                 continue
    #             for x3 in range(x2 + 1, width):
    #                 if y1 + 1 in obstacles_x[x3]:
    #                     loop_blocks.add((x3 + 1, y2 + 1))
    #                 elif y2 - 1 in obstacles_x[x3]:
    #                     loop_blocks.add((x3 - 1, y1 + 1))

    # return len(loop_blocks)

    # OPTION THREE (FAILS)
    # same as optiopn one, but imagines further to try for loops
    # grid: list[list[chr]] = []
    # guard_pos = None, None
    # guard_dir = None
    # line, y = "", 0
    # for line in data:
    #     grid.append(list(line))
    #     if match := re.search(r"\^|>|v|<", line):
    #         guard_dir = match.group()
    #         guard_pos = match.span()[0], y
    #     y += 1

    # width = len(line)
    # height = y

    # guard_passed: list[tuple[chr, tuple[int]]] = []
    # guard_passed.append((guard_dir, guard_pos))

    # # we need a function that, given a grid and the position history of the
    # # guard, determines if the guard would fall into their own footsteps again
    # def loops(grid, guard_passed):
    #     guard_dir = guard_passed[-1][0]
    #     guard_pos = guard_passed[-1][1]

    #     while True:
    #         # let's walk
    #         guard_pos = (
    #             guard_pos[0] + DELTAS[guard_dir][0],
    #             guard_pos[1] + DELTAS[guard_dir][1],
    #         )

    #         # we were here before!
    #         if (guard_dir, guard_pos) in guard_passed:
    #             return True

    #         # we fall off the board
    #         if (
    #             -1 in guard_pos
    #             or guard_pos[0] >= width
    #             or guard_pos[1] >= height
    #         ):
    #             return False
    #         # we bump into an obstacle
    #         if grid[guard_pos[1]][guard_pos[0]] == "#":
    #             guard_pos = (
    #                 guard_pos[0] - DELTAS[guard_dir][0],
    #                 guard_pos[1] - DELTAS[guard_dir][1],
    #             )
    #             guard_dir = DIRS[(DIRS.index(guard_dir) + 1) % len(DIRS)]

    #         guard_passed.append((guard_dir, guard_pos))

    # loop_blocks = set()
    # index= 0
    # while True:
    #     index += 1
    #     print(f"step {index}/4776", end="\r")
    #     # let's imagine we turn right here
    #     imagined_dir = DIRS[(DIRS.index(guard_dir) + 1) % len(DIRS)]
    #     if loops(grid, guard_passed.copy()[:-1] + [(imagined_dir, guard_pos)]):
    #         loop_blocks.add(
    #             (
    #                 guard_pos[0] + DELTAS[guard_dir][0],
    #                 guard_pos[1] + DELTAS[guard_dir][1],
    #             )
    #         )

    #     # now stop imagining, and walk for real
    #     new_pos = (
    #         guard_pos[0] + DELTAS[guard_dir][0],
    #         guard_pos[1] + DELTAS[guard_dir][1],
    #     )

    #     if -1 in new_pos or new_pos[0] >= width or new_pos[1] >= height:
    #         break

    #     if grid[new_pos[1]][new_pos[0]] == "#":
    #         guard_dir = DIRS[(DIRS.index(guard_dir) + 1) % len(DIRS)]
    #     else:
    #         guard_pos = new_pos
    #         guard_passed.append((guard_dir, guard_pos))

    # return len(loop_blocks)
