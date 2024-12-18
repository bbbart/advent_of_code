#!/usr/bin/env python

from collections import defaultdict
from itertools import product


# pylint: disable=too-many-branches,too-many-statements,too-many-locals
def p1(data: list[str], is_sample: bool):
    # parse the input data
    for x, line in enumerate(data):
        try:
            source = (x, line.index("S"))
        except ValueError:
            pass
        try:
            sink = (x, line.index("E"))
        except ValueError:
            pass

    width = len(data[0])

    # store the maze as a graph of corners
    # find horizontal edges
    graph = defaultdict(list)
    for x, line in enumerate(data):
        corner_left, corner_right = None, None
        for y, char in enumerate(line):
            if char == "#":
                corner_left, corner_right = None, None
                continue
            if data[x - 1][y] == "." or data[x + 1][y] == ".":
                if not corner_left:
                    corner_left = (x, y)
                else:
                    corner_right = (x, y)
                    graph[corner_left].append(corner_right)
                    graph[corner_right].append(corner_left)
                    corner_left, corner_right = corner_right, None

    # find vertical edges
    for y in range(width):
        corner_top, corner_bottom = None, None
        for x, line in enumerate(data):
            if line[y] == "#":
                corner_top, corner_bottom = None, None
                continue
            if line[y - 1] == "." or line[y + 1] == "." or line[y] in "SE":
                if not corner_top:
                    corner_top = (x, y)
                else:
                    corner_bottom = (x, y)
                    graph[corner_top].append(corner_bottom)
                    graph[corner_bottom].append(corner_top)
                    corner_top, corner_bottom = corner_bottom, None

    # find the shortest path
    def neighbours(pos):
        for n in graph[pos[0]]:
            x_dist = n[0] - pos[0][0]
            y_dist = n[1] - pos[0][1]
            direction = (
                (x_dist // abs(x_dist)) if x_dist else 0,
                (y_dist // abs(y_dist)) if y_dist else 0,
            )
            if direction == pos[1]:
                yield abs(x_dist) + abs(y_dist), (n, direction)
            elif direction[0] + direction[0] + direction[1] + direction[1] == 0:
                continue
            else:
                yield 1000 + abs(x_dist) + abs(y_dist), (n, direction)

    to_explore = set(product(graph.keys(), [(0, 1), (-1, 0), (0, -1), (1, 0)]))
    distance = defaultdict(lambda: float("inf"))
    prev = {}

    distance[source, (0, 1)] = 0
    while to_explore:
        pos = min(to_explore, key=distance.__getitem__)
        to_explore.remove(pos)

        for cost, new_pos in neighbours(pos):
            if distance[new_pos] > distance[pos] + cost:
                distance[new_pos] = distance[pos] + cost
                prev[new_pos] = pos

    return min(distance[p] for p in distance if p[0] == sink)

def p2(data: list[str], is_sample: bool):
    # tried brute forcing, but that took way too long
    return "N/A"
