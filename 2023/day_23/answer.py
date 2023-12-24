#!/usr/bin/env python


import sys
from collections import defaultdict
from itertools import pairwise


def set_scenery(data):
    scenery = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            scenery[(x, y)] = char
            if char == ".":
                if y == 0:
                    start_pos = (x, y)
                else:
                    end_pos = (x, y)
    return scenery, start_pos, end_pos


def p1(data, is_sample):
    scenery, start_pos, end_pos = set_scenery(data)

    graph: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for pos in scenery:
        for d in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            neighbour = tuple(x + y for x, y in zip(pos, d))
            match (d, scenery.get(neighbour, None)):
                case (_, ".") | ((1, 0), ">") | ((0, 1), "v") | (
                    (-1, 0),
                    "<",
                ) | ((0, -1), "^"):
                    graph[pos].add(neighbour)

    def DFS(u, v):
        if u in visited:
            return
        visited.add(u)

        current_path.append(u)

        if u == v:
            simple_paths.append(current_path[:])
            visited.remove(u)
            current_path.pop(-1)
            return

        for n in graph[u]:
            DFS(n, v)

        current_path.pop(-1)
        visited.remove(u)

    visited = set()
    current_path = []
    simple_paths = []

    sys.setrecursionlimit(2500)  # is this cheating ;-)
    DFS(start_pos, end_pos)

    return max(len(p) for p in simple_paths) - 1


def p2(data, is_sample):
    # scan the data
    scenery, start_pos, end_pos = set_scenery(data)

    # build a naive graph
    graph: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for pos in scenery:
        for d in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            neighbour = tuple(x + y for x, y in zip(pos, d))
            if scenery.get(neighbour, "#") != "#":
                graph[pos].add(neighbour)

    # break up the graph in 'roads', strings of adjacent cells (vertices)
    def follow_road(u, v):
        if (u, v) in visited:
            return
        visited.add((u, v))

        path = [u, v]
        n = graph[v] - {u}
        while len(n) == 1:
            u = v
            v = n.pop()
            path.append(v)
            n = graph[v] - {u}
        roads.append(path)
        while n:
            follow_road(v, n.pop())

    roads = []
    visited = set()
    follow_road(start_pos, graph[start_pos].pop())

    # use the road information to but a much more condensed graph, connecting
    # crossroads and recording the steps required to go from on to another
    cgraph: dict[
        tuple[int, int], set[tuple[tuple[int, int], int]]
    ] = defaultdict(set)
    for road in roads:
        cgraph[road[0]].add((road[-1], len(road) - 1))

    # use the exact same algorithm as p1 to find all possible paths from
    # start_pos to end_pos
    def DFS(u, v):
        if u in visited:
            return
        visited.add(u)

        current_path.append(u)

        if u == v:
            simple_paths.append(current_path[:])
            visited.remove(u)
            current_path.pop(-1)
            return

        for n in cgraph[u]:
            DFS(n[0], v)

        current_path.pop(-1)
        visited.remove(u)

    visited = set()
    current_path = []
    simple_paths = []
    DFS(start_pos, end_pos)

    # select the longest path from all those found above
    def steps(path):
        step_counter = 0
        for f, t in pairwise(path):
            for p in cgraph[f]:
                if p[0] == t:
                    step_counter += p[1]
        return step_counter

    return max(steps(p) for p in simple_paths)
