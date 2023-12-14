#!/usr/bin/env python

from copy import deepcopy


def show_platform(balls, rocks):
    width = max(
        max(max(b) for b in balls.values() if b), max(r[0] for r in rocks)
    ) + 1
    height = max(max(balls), max(r[1] for r in rocks)) + 1
    for y in range(height):
        line = ""
        for x in range(width):
            if x in balls[y]:
                line += "O"
            elif (x, y) in rocks:
                line += "#"
            else:
                line += "."
        print(line)


def tilt_north(balls, rocks):
    for y in sorted(balls):
        for x in tuple(balls[y]):
            for i in range(1, y + 1):
                if x in balls[y - i] or (x, y - i) in rocks:
                    balls[y].remove(x)
                    balls[y - i + 1].add(x)
                    break
            else:
                balls[y].remove(x)
                balls[0].add(x)


def tilt_west(balls, rocks):
    for y in balls:
        for x in sorted(balls[y]):
            for i in range(1, x + 1):
                if x - i in balls[y] or (x - i, y) in rocks:
                    balls[y].remove(x)
                    balls[y].add(x - i + 1)
                    break
            else:
                balls[y].remove(x)
                balls[y].add(0)


def tilt_south(balls, rocks):
    max_y = max(max(balls), max(r[1] for r in rocks))
    for y in reversed(balls):
        for x in tuple(balls[y]):
            for i in range(1, max_y + 1 - y):
                if x in balls[y + i] or (x, y + i) in rocks:
                    balls[y].remove(x)
                    balls[y + i - 1].add(x)
                    break
            else:
                balls[y].remove(x)
                balls[max_y].add(x)


def tilt_east(balls, rocks):
    max_x = max(
        max(max(b) for b in balls.values() if b), max(r[0] for r in rocks)
    )
    for y in balls:
        for x in reversed(sorted(balls[y])):
            for i in range(1, max_x + 1 - x):
                if x + i in balls[y] or (x + i, y) in rocks:
                    balls[y].remove(x)
                    balls[y].add(x + i - 1)
                    break
            else:
                balls[y].remove(x)
                balls[y].add(max_x)


def p1(data, is_sample):
    rocks = set()
    balls = {}

    y = 0
    for y, line in enumerate(data):
        balls[y] = set()
        for x, char in enumerate(line):
            match char:
                case "#":
                    rocks.add((x, y))
                case "O":
                    balls[y].add(x)
    height = y + 1

    tilt_north(balls, rocks)

    return sum((height - y) * len(b) for y, b in balls.items())


def p2(data, is_sample):
    rocks = set()
    balls = {}

    y = 0
    width = 0
    for y, line in enumerate(data):
        balls[y] = set()
        for x, char in enumerate(line):
            match char:
                case "#":
                    rocks.add((x, y))
                case "O":
                    balls[y].add(x)
            width = max(width, x + 1)
    height = y + 1

    ball_arrangements = []
    cycle_target = 1_000_000_000
    for _ in range(cycle_target):
        tilt_north(balls, rocks)
        tilt_west(balls, rocks)
        tilt_south(balls, rocks)
        tilt_east(balls, rocks)
        if balls in ball_arrangements:
            break
        ball_arrangements.append(deepcopy(balls))
    else:
        return sum((height - y) * len(b) for y, b in balls.items())

    # we broke out of the for: loop detected!
    loop_start = ball_arrangements.index(balls)
    loop_period = len(ball_arrangements) - loop_start

    balls = ball_arrangements[
        loop_start + (cycle_target - loop_start) % loop_period - 1
    ]

    return sum((height - y) * len(b) for y, b in balls.items())
