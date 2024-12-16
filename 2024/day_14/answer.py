#!/usr/bin/env python

import re
from collections import Counter
from functools import reduce


def visualize(robots, w, h, s=0):
    locs = Counter(
        ((r[0] + s * r[2]) % w, (r[1] + s * r[3]) % h) for r in robots
    )
    for y in range(h):
        print("\n")
        if y == h // 2:
            continue
        for x in range(w):
            if x == w // 2:
                print(" ", end="")
                continue
            if (x, y) in locs:
                print(locs[(x, y)], end="")
            else:
                print(".", end="")


def p1(data: list[str], is_sample: bool):
    if not is_sample:
        width = 101
        height = 103
    else:
        width = 11
        height = 7

    robots = set()
    Qs: list[int] = [0, 0, 0, 0]
    robots = set()
    for line in data:
        robot = tuple(
            map(
                int,
                re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line).groups(),
            )
        )
        robots.add(robot)
        pos_100 = (
            (robot[0] + 100 * robot[2]) % width,
            (robot[1] + 100 * robot[3]) % height,
        )
        if pos_100[0] < width // 2 and pos_100[1] < height // 2:
            Qs[0] += 1
        elif pos_100[0] > width // 2 and pos_100[1] < height // 2:
            Qs[1] += 1
        elif pos_100[0] > width // 2 and pos_100[1] > height // 2:
            Qs[2] += 1
        elif pos_100[0] < width // 2 and pos_100[1] > height // 2:
            Qs[3] += 1

    # visualize(robots, width, height, s=100)

    return reduce(lambda x, y: x * y, Qs)


def p2(data: list[str], is_sample: bool):
    if is_sample:
        return "N/A"

    width = 101
    height = 103

    robots = set()
    for line in data:
        robot = tuple(
            map(
                int,
                re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line).groups(),
            )
        )
        robots.add(robot)

    s = 0
    while True:
        pos_s = {
            ((r[0] + s * r[2]) % width - width // 2, (r[1] + s * r[3]) % height)
            for r in robots
        }
        # we're assuming the christmas tree has horizontal symmetry
        # hmmm... but the challenge states "MOST of the robots should arrange
        # themselves"...
        for p in pos_s:
            if not (-p[0], p[1]) in pos_s:
                s+= 1
                break
        else:
            visualize(robots, width, height, s)
            return s
