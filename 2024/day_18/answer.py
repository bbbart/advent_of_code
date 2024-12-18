#!/usr/bin/env python

from collections import defaultdict


def path_to_exit(corrupted, size, count):
    corrupted = set(corrupted[:count])

    def neighbours(pos: tuple[int]):
        x, y = pos
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            newpos = x + dx, y + dy
            if (
                newpos not in corrupted
                and newpos[0] >= 0
                and newpos[1] >= 0
                and newpos[0] < size
                and newpos[1] < size
            ):
                yield x + dx, y + dy

    start = 0, 0
    end = size - 1, size - 1

    distance = defaultdict(lambda: float("inf"))
    prev = {}
    to_visit = {(x, y) for x in range(size) for y in range(size)} - corrupted

    distance[start] = 0
    while to_visit:
        pos = min(to_visit, key=lambda p: distance[p])
        to_visit.remove(pos)

        for new_pos in neighbours(pos):
            if new_pos not in to_visit:
                continue
            new_distance = distance[pos] + 1
            if new_distance < distance[new_pos]:
                distance[new_pos] = new_distance
                prev[new_pos] = pos

    path = []
    pos = end
    while pos != start:
        path.insert(0, pos)
        pos = prev[pos]

    return path


def p1(data: list[str], is_sample: bool):
    if not is_sample:
        size = 71
        count = 1024
    else:
        size = 7
        count = 12

    corrupted = []
    for line in data:
        corrupted.append(tuple(map(int, line.split(","))))

    return len(path_to_exit(corrupted, size, count))


def p2(data: list[str], is_sample: bool):
    if not is_sample:
        size = 71
        min_count = 1024
    else:
        size = 7
        min_count = 12

    corrupted = []
    for line in data:
        corrupted.append(tuple(map(int, line.split(","))))

    max_count = len(corrupted) - 1
    while True:
        count = min_count + (max_count - min_count) // 2
        try:
            path_to_exit(corrupted, size, count)
            min_count = count
        except KeyError:
            max_count = count

        if max_count - min_count < 2:
            return corrupted[max_count - 1]
