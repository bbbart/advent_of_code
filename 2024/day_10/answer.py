#!/usr/bin/env python

from collections import defaultdict, deque


def p1(data: list[str], is_sample: bool):
    # parse the map
    topo: dict[int, set[tuple[int]]] = defaultdict(set)
    y = 0
    for line in data:
        x = 0
        for char in line:
            topo[int(char)].add((x, y))
            x += 1
        y += 1

    # build the graph
    steps = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    graph = defaultdict(set)
    for n in range(9):
        for loc in topo[n]:
            for s in steps:
                neighbour = (loc[0] + s[0], loc[1] + s[1])
                if neighbour in topo[n + 1]:
                    graph[loc].add(neighbour)

    # walk the graph
    def find_peaks(start: tuple[int, int]):
        to_do = deque()
        to_do.append(start)
        while to_do:
            loc = to_do.popleft()
            if loc in topo[9]:
                yield loc
            to_do.extend(graph[loc])

    return sum(len(set(find_peaks(trailhead))) for trailhead in topo[0])


def p2(data: list[str], is_sample: bool):
    # parse the map
    topo: dict[int, set[tuple[int]]] = defaultdict(set)
    y = 0
    for line in data:
        x = 0
        for char in line:
            topo[int(char)].add((x, y))
            x += 1
        y += 1

    # build the graph
    steps = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    graph = defaultdict(set)
    for n in range(9):
        for loc in topo[n]:
            for s in steps:
                neighbour = (loc[0] + s[0], loc[1] + s[1])
                if neighbour in topo[n + 1]:
                    graph[loc].add(neighbour)

    # walk the graph
    def find_peaks(start: tuple[int, int]):
        to_do = deque()
        to_do.append(start)
        while to_do:
            loc = to_do.popleft()
            if loc in topo[9]:
                yield loc
            to_do.extend(graph[loc])

    return sum(len(list(find_peaks(trailhead))) for trailhead in topo[0])
