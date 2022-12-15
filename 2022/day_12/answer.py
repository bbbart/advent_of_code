from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from string import ascii_lowercase
from warnings import warn


@dataclass
class Node:
    x: int
    y: int
    height: str

    def __hash__(self):
        return hash(f"{self.x}{self.y}")


def char_to_height(char):
    if char == "S":
        char = "a"
    elif char == "E":
        char = "z"

    return ascii_lowercase.index(char)


def get_neighbours(node, area):
    for x, y in (
        (node.x - 1, node.y),
        (node.x + 1, node.y),
        (node.x, node.y - 1),
        (node.x, node.y + 1),
    ):
        if x < 0 or y < 0:
            continue

        try:
            yield area[y][x]
        except IndexError:
            continue


def build_graph(data):
    # read all data in a matrix like structure
    area = []
    pos_x, pos_y = 0, 0
    start, goal = None, None
    for line in data:
        area_line = []
        pos_x = 0
        for char in line:
            height = char_to_height(char)
            node = Node(pos_x, pos_y, height)
            if char == "S":
                start = node
            elif char == "E":
                goal = node
            area_line.append(node)
            pos_x += 1
        area.append(area_line)
        pos_y += 1

    # build the graph
    graph = defaultdict(list)
    for area_line in area:
        for node in area_line:
            for neighbour in get_neighbours(node, area):
                if neighbour.height <= node.height + 1:
                    graph[node].append(neighbour)

    return start, goal, graph


def find_shortest_path(start, goal, graph):
    # simple breadth-first search (recursion with memoization would have been
    # faster)
    explored = []
    queue = [[start]]

    if start == goal:
        return [start]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node in explored:
            continue

        for neighbour in graph[node]:
            new_path = deepcopy(path)
            new_path.append(neighbour)
            queue.append(new_path)

            if neighbour == goal:
                return new_path

        explored.append(node)

    warn("No path found! :-()")
    return None


def p1(data, is_sample):
    start, goal, graph = build_graph(data)
    path = find_shortest_path(start, goal, graph)
    return len(path) - 1


def p2(data, is_sample):
    _, goal, graph = build_graph(data)
    scenic_paths = []
    for start in graph.keys():
        if start.height == 0:
            path = find_shortest_path(start, goal, graph)
            if path:
                scenic_paths.append(path)

    return min(len(path) for path in scenic_paths) - 1
