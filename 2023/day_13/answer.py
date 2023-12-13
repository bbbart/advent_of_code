#!/usr/bin/env python

from collections import defaultdict


def find_mirrors(block: set) -> int:
    xs = defaultdict(set)
    ys = defaultdict(set)

    for co_x, co_y in block:
        ys[co_x].add(co_y)
        xs[co_y].add(co_x)

    height = max(xs)
    width = max(ys)

    # look for vertical mirrors
    v_mirrors = []
    for x in range(width):
        if all(
            ys[x - i] == ys[x + i + 1]
            for i in range(min(abs(width - x), x + 1))
        ):
            v_mirrors.append(x + 1)

    # look for horizontal mirrors
    h_mirrors = []
    for y in range(height):
        if all(
            xs[y - i] == xs[y + i + 1]
            for i in range(min(abs(height - y), y + 1))
        ):
            h_mirrors.append(y + 1)

    return sum(v_mirrors) + 100 * sum(h_mirrors)


def find_almost_mirrors(block: set):
    xs = defaultdict(set)
    ys = defaultdict(set)

    for co_x, co_y in block:
        ys[co_x].add(co_y)
        xs[co_y].add(co_x)

    height = max(xs)
    width = max(ys)

    # look for almost vertical mirrors
    almost_v_mirrors = []
    for x in range(width):
        differences = 0
        for i in range(min(abs(width - x), x + 1)):
            above = ys[x - i]
            below = ys[x + i + 1]
            differences += len(set.union(above - below, below - above))
            if differences > 1:
                break
        else:
            if differences == 1:
                almost_v_mirrors.append(x + 1)

    # look for almost horizontal mirrors
    almost_h_mirrors = []
    for y in range(height):
        differences = 0
        for i in range(min(abs(height - y), y + 1)):
            left = xs[y - i]
            right = xs[y + i + 1]
            differences += len(set.union(right - left, left - right))
            if differences > 1:
                break
        else:
            if differences == 1:
                almost_h_mirrors.append(y + 1)

    return sum(almost_v_mirrors) + 100 * sum(almost_h_mirrors)


def p1(data, is_sample):
    block: set[tuple[int, int]] = set()
    blocks = []
    y = 0
    for line in data:
        if not line:
            blocks.append(block)
            block = set()
            y = 0
            continue
        assert "#" in line
        for x, char in enumerate(line):
            if char == "#":
                block.add((x, y))
        y += 1
    blocks.append(block)

    answer = 0
    for block in blocks:
        answer += find_mirrors(block)

    return answer


def p2(data, is_sample):
    block: set[tuple[int, int]] = set()
    blocks = []
    y = 0
    for line in data:
        if not line:
            blocks.append(block)
            block = set()
            y = 0
            continue
        assert "#" in line
        for x, char in enumerate(line):
            if char == "#":
                block.add((x, y))
        y += 1
    blocks.append(block)

    answer = 0
    for block in blocks:
        answer += find_almost_mirrors(block)

    return answer
