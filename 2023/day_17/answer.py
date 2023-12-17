#!/usr/bin/env python

from collections import defaultdict
from queue import Empty, PriorityQueue

deltas = {"r": (1, 0), "d": (0, 1), "l": (-1, 0), "u": (0, -1)}


def modified_dijkstra_p1(graph, start, goal, neighbour_function):
    to_explore = PriorityQueue()
    to_explore.put((0, start, [""]))
    visited = defaultdict(lambda: float("inf"))

    width = max(node[0] for node in graph) + 1
    height = max(node[1] for node in graph) + 1

    while True:
        try:
            current_loss, current_block, current_path = to_explore.get_nowait()
        except Empty:
            break

        if current_block == goal:
            return current_loss

        for direction, next_block in neighbour_function(
            current_block, current_path, width, height
        ):
            next_loss = current_loss + graph[next_block]
            next_path = current_path + [direction]
            if (
                visited[(next_block, tuple(current_path[-3:] + [direction]))]
                > next_loss
            ):
                to_explore.put((next_loss, next_block, next_path))
                visited[
                    (next_block, tuple(current_path[-3:] + [direction]))
                ] = next_loss

    return float("inf")


def modified_dijkstra_p2(graph, start, goal, neighbour_function):
    to_explore = PriorityQueue()
    to_explore.put((0, start, [""]))
    visited = defaultdict(lambda: float("inf"))

    width = max(node[0] for node in graph) + 1
    height = max(node[1] for node in graph) + 1

    while True:
        try:
            current_loss, current_block, current_path = to_explore.get_nowait()
        except Empty:
            break

        if current_block == goal:
            if len(set(current_path[-4:])) == 1:
                return current_loss
            continue

        for direction, next_block in neighbour_function(
            current_block, current_path, width, height
        ):
            next_loss = current_loss + graph[next_block]
            next_path = current_path + [direction]
            if (
                visited[(next_block, tuple(current_path[-9:] + [direction]))]
                > next_loss
            ):
                to_explore.put((next_loss, next_block, next_path))
                visited[
                    (next_block, tuple(current_path[-9:] + [direction]))
                ] = next_loss

    return float("inf")


def p1(data, is_sample):
    heatloss: dict[tuple[int, int], int] = {}
    x, y = 0, 0
    for y, line in enumerate(data):
        for x, loss in enumerate(line):
            heatloss[(x, y)] = int(loss)

    start = (0, 0)
    goal = (x, y)

    def neighbours(block, path, width, height):
        for direction, delta in deltas.items():
            # cannot move to the same direction more than three times in a row
            if path[-3:] == [direction] * 3:
                continue

            # cannot go back where we came from
            try:
                if {path[-1], direction} in (
                    {"l", "r"},
                    {"u", "d"},
                ):
                    continue
            except IndexError:
                pass

            neighbour = tuple(x + y for x, y in zip(block, delta))

            # cannot move out of bounds
            if (
                min(neighbour) < 0
                or neighbour[0] >= width
                or neighbour[1] >= height
            ):
                continue

            yield direction, neighbour

    return modified_dijkstra_p1(heatloss, start, goal, neighbours)


def p2(data, is_sample):
    heatloss: dict[tuple[int, int], int] = {}
    x, y = 0, 0
    for y, line in enumerate(data):
        for x, loss in enumerate(line):
            heatloss[(x, y)] = int(loss)

    start = (0, 0)
    goal = (x, y)

    def neighbours(block, path, width, height):
        last_four_directions = set(path[-4:])

        for direction, delta in deltas.items():
            # have to move to the same direction at least four times in a row
            if len(last_four_directions) > 1 and direction != path[-1]:
                continue

            # cannot move to the same direction more than ten times in a row
            if path[-10:] == [direction] * 10:
                continue

            # cannot go back where we came from
            try:
                if {path[-1], direction} in (
                    {"l", "r"},
                    {"u", "d"},
                ):
                    continue
            except IndexError:
                pass

            neighbour = tuple(x + y for x, y in zip(block, delta))

            # cannot move out of bounds
            if (
                min(neighbour) < 0
                or neighbour[0] >= width
                or neighbour[1] >= height
            ):
                continue

            yield direction, neighbour

    return modified_dijkstra_p2(heatloss, start, goal, neighbours)
