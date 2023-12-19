#!/usr/bin/env python

from dataclasses import dataclass
from queue import Empty, PriorityQueue
from collections import defaultdict
from itertools import filterfalse


def show_trench(walls):
    for y in range(min(w[1] for w in walls), max(w[1] for w in walls) + 1):
        print()
        for x in range(min(w[0] for w in walls), max(w[0] for w in walls) + 1):
            print(walls[(x, y)] if (x, y) in walls else ".", end="")


def count_inside_p1(walls):
    # figure out how many tiles are inside; this implements a simple
    # line sweep algorithm (taken from 2023/day_10)
    in_counter = 0
    for y in range(min(w[1] for w in walls), max(w[1] for w in walls) + 1):
        inout = False
        horizontal_wall = ""
        for x in range(min(w[0] for w in walls), max(w[0] for w in walls) + 1):
            # if we encounter a tile not part of the loop, our state doesn't
            # change, but our counter (potentially) does
            if (x, y) not in walls:
                in_counter += 1 if inout else 0
                # print("I" if inout else ".", end="")
                continue

            # if we encounter a tile part of the loop, our state changes, but
            # our counter doesn't
            char = walls[(x, y)]
            if char == "|":
                inout = not inout
            else:
                horizontal_wall += char

            if char in ("7", "J"):
                if (
                    horizontal_wall.startswith("F")
                    and horizontal_wall.endswith("J")
                ) or (
                    horizontal_wall.startswith("L")
                    and horizontal_wall.endswith("7")
                ):
                    # a 'winding' horizontal_wall, not a 'looping'
                    # horizontal_wall
                    inout = not inout
                horizontal_wall = ""

    return in_counter


def p1(data, is_sample):
    instructions = []
    for line in data:
        instruction = line.split()
        instructions.append((instruction[0], int(instruction[1])))

    x, y = 0, 0
    trench_wall = {}
    for i, instruction in enumerate(instructions):
        if (instructions[i - 1][0] == "U" and instruction[0] == "R") or (
            instructions[i - 1][0] == "L" and instruction[0] == "D"
        ):
            corner = "F"
        elif (instructions[i - 1][0] == "U" and instruction[0] == "L") or (
            instructions[i - 1][0] == "R" and instruction[0] == "D"
        ):
            corner = "7"
        elif (instructions[i - 1][0] == "D" and instruction[0] == "R") or (
            instructions[i - 1][0] == "L" and instruction[0] == "U"
        ):
            corner = "L"
        elif (instructions[i - 1][0] == "D" and instruction[0] == "L") or (
            instructions[i - 1][0] == "R" and instruction[0] == "U"
        ):
            corner = "J"

        trench_wall[(x, y)] = corner
        if instruction[0] in ("R", "L"):
            for _ in range(instruction[1]):
                x += -1 if instruction[0] == "L" else 1
                if any((x, y)):
                    trench_wall[(x, y)] = "-"
        elif instruction[0] in ("U", "D"):
            for _ in range(instruction[1]):
                y += -1 if instruction[0] == "U" else 1
                if any((x, y)):
                    trench_wall[(x, y)] = "|"

    return count_inside_p1(trench_wall) + len(trench_wall)


@dataclass
class Rectangle:
    tlc: tuple[int, int] = (None, None)
    brc: tuple[int, int] = (None, None)

    @property
    def trc(self):
        return (self.brc[0], self.tlc[1])

    @property
    def blc(self):
        return (self.tlc[0], self.brc[1])

    @property
    def area(self):
        if not self.closed:
            return None
        return abs(self.brc[0] - self.tlc[0]) * abs(self.brc[1] - self.tlc[1])

    @property
    def closed(self):
        return not None in self.tlc and not None in self.brc


def p2(data, is_sample):
    # the algorithm below actually works, if you consider the lines surrounding
    # the shape no width themselves. so, for a mathematical shape (with the
    # same constraints), it calculates the area, given the coordinates of the
    # corners, just fine.
    #
    # however, in the AoC problem, this is not the case. I expect this can be
    # made to work with a 'alternative' coordinate system, for the lines
    # between the dug trenches (#), instead of the trenches themselves
    return 'incomplete'

    instructions = []
    for line in data:
        if not line:
            break
        instruction = line.split()[-1]
        instructions.append(
            ("RDLU"[int(instruction[7])], int(instruction[2:7], 16))
        )

    # get the coordinates of the corners of the trench shape
    x, y = 0, 0
    corners = PriorityQueue()
    shapes = defaultdict(str)
    for i, instruction in enumerate(instructions):
        if (instructions[i - 1][0] == "U" and instruction[0] == "R") or (
            instructions[i - 1][0] == "L" and instruction[0] == "D"
        ):
            shape = "F"
        elif (instructions[i - 1][0] == "U" and instruction[0] == "L") or (
            instructions[i - 1][0] == "R" and instruction[0] == "D"
        ):
            shape = "7"
        elif (instructions[i - 1][0] == "D" and instruction[0] == "R") or (
            instructions[i - 1][0] == "L" and instruction[0] == "U"
        ):
            shape = "L"
        elif (instructions[i - 1][0] == "D" and instruction[0] == "L") or (
            instructions[i - 1][0] == "R" and instruction[0] == "U"
        ):
            shape = "J"

        corners.put((x, y))
        shapes[(x, y)] = shape

        if instruction[0] in ("R", "L"):
            x += (-1 if instruction[0] == "L" else 1) * instruction[1]
        elif instruction[0] in ("U", "D"):
            y += (-1 if instruction[0] == "U" else 1) * instruction[1]

    assert (x, y) == (0, 0)

    # partition the shape into rectangles
    rectangles = []
    corners_seen = set()
    while True:
        try:
            (co_x, co_y) = corners.get_nowait()
        except Empty:
            break

        if (co_x, co_y) in corners_seen:
            continue
        corners_seen.add((co_x, co_y))

        for r in filterfalse(lambda r: r.closed, rectangles):
            if co_y in (r.tlc[1], r.brc[1]):
                r.brc = (co_x, r.brc[1])
                if r.closed:
                    if r.brc not in corners_seen:
                        corners.put(r.brc)
                    if r.trc not in corners_seen:
                        corners.put(r.trc)
                break
            if co_x in (r.tlc[0], r.brc[0]):
                if not shapes[(co_x, co_y)] in ('J', 'F'):
                    r.brc = (r.brc[0], co_y)
                    if r.closed:
                        if r.brc not in corners_seen:
                            corners.put(r.brc)
                        if r.trc not in corners_seen:
                            corners.put(r.trc)
                    break
        else:
            # we start a new rectangle
            r = Rectangle()
            r.tlc = (co_x, co_y)
            rectangles.append(r)

    # add the ares of the partition rectangles
    return sum(r.area for r in rectangles if r.closed)
