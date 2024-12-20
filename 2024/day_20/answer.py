#!/usr/bin/env python

import sys
from collections import defaultdict
from itertools import combinations

sys.setrecursionlimit(30_000)


# pylint: disable=too-many-locals
def p1(data: list[str], is_sample: bool):
    return "disabled"
    start_pos, end_pos = None, None
    walls = set()
    fair_time = 0
    width = len(data[0])
    height = len(data)
    for x, line in enumerate(data):
        for y, char in enumerate(line):
            match char:
                case "S":
                    start_pos = x, y
                case "E":
                    end_pos = x, y
                    fair_time += 1
                case "#":
                    walls.add((x, y))
                case ".":
                    fair_time += 1

    # one by one, we will treat the grid as if a wall cell is not there. then
    # we calculate the fastest path from S to E, given the new scenario. this
    # should be pretty fast, given that all but one cell (the one where we
    # cheat) will have only a single undiscovered neighbour
    #
    # we can only read from the cache *after* the cheat, since before it, our
    # walls are different then when we entered the value in the cache
    def shortest_path(start_pos, cheat_pos=None):
        time = defaultdict(lambda: float("inf"))
        prev = {}
        queue = {
            (i, j)
            for i in range(height)
            for j in range(width)
            if (i, j) not in walls
        }
        time[start_pos] = 0

        while queue:
            x, y = min(queue, key=time.__getitem__)
            queue.remove((x, y))
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in walls or (nx, ny) not in queue:
                    continue
                if time[(nx, ny)] < time[(x, y)] + 1:
                    continue
                time[(nx, ny)] = time[(x, y)] + 1
                prev[(nx, ny)] = (x, y)
                if (nx, ny) == end_pos:
                    queue.clear()
                    break
            if (x, y) == cheat_pos:
                queue.clear()
                break

        path = []
        prev_pos = (x, y)
        path.append(prev_pos)
        while (prev_pos := prev.get(prev_pos)) != start_pos:
            path.append(prev_pos)
        return path

    fair_path = shortest_path(start_pos)
    fair_path.insert(0, end_pos)
    fair_path.append(start_pos)

    good_cheats = 0
    for cheat in walls.copy():
        if not (0 < cheat[0] < width - 1 and 0 < cheat[1] < height - 1):
            # we don't cheat through borders
            continue

        cheat_neighbour_cells = [
            (cheat[0] + dx, cheat[1] + dy)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        ]
        cheat_neighbour_cells = tuple(
            cell
            for cell in cheat_neighbour_cells
            if data[cell[0]][cell[1]] in ".SE"
        )

        for cheat_path in combinations(cheat_neighbour_cells, 2):
            first = max(cheat_path, key=fair_path.index)
            last = min(cheat_path, key=fair_path.index)
            cheat_time = (
                len(fair_path)
                + fair_path.index(last)
                - fair_path.index(first)
                + 1
            )
            if fair_time - cheat_time >= 100:
                good_cheats += 1

    return good_cheats


# pylint: disable=too-many-locals
def p2(data: list[str], is_sample: bool):
    # if not is_sample:
    #     return "N/A"

    # parsing the data
    start_pos, end_pos = None, None
    walls = set()
    fair_time = 0
    width = len(data[0])
    height = len(data)
    for x, line in enumerate(data):
        for y, char in enumerate(line):
            match char:
                case "S":
                    start_pos = x, y
                case "E":
                    end_pos = x, y
                    fair_time += 1
                case "#":
                    walls.add((x, y))
                case ".":
                    fair_time += 1

    def shortest_path(start_pos, cheat_pos=None):
        time = defaultdict(lambda: float("inf"))
        prev = {}
        queue = {
            (i, j)
            for i in range(height)
            for j in range(width)
            if (i, j) not in walls
        }
        time[start_pos] = 0

        while queue:
            x, y = min(queue, key=time.__getitem__)
            queue.remove((x, y))
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in walls or (nx, ny) not in queue:
                    continue
                if time[(nx, ny)] < time[(x, y)] + 1:
                    continue
                time[(nx, ny)] = time[(x, y)] + 1
                prev[(nx, ny)] = (x, y)
                if (nx, ny) == end_pos:
                    queue.clear()
                    break
            if (x, y) == cheat_pos:
                queue.clear()
                break

        path = []
        prev_pos = (x, y)
        path.append(prev_pos)
        while (prev_pos := prev.get(prev_pos)) != start_pos:
            path.append(prev_pos)

        return path

    fair_path = shortest_path(start_pos)
    fair_path.insert(0, end_pos)
    fair_path.append(start_pos)

    def dfs(current, target, max_length, path_length=0, visited=None):
        if visited is None:
            visited = set()

        if path_length > max_length:
            return False

        if current == target:
            return path_length

        visited.add(current)

        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            neighbour_pos = current[0] + dx, current[1] + dy
            if not (
                0 < neighbour_pos[0] < height - 1
                and 0 < neighbour_pos[1] < width - 1
            ):
                continue
            neighbour = data[neighbour_pos[0]][neighbour_pos[1]]
            if neighbour not in "#E" or neighbour_pos in visited:
                continue
            if path_length := dfs(
                neighbour_pos, target, max_length, path_length + 1, visited
            ):
                return path_length

        visited.remove(current)

        return False

    # stategy: for each cell on the fair path, figure out if there is another
    # cell we can reach only by passing to max 19 walls that is more than 100
    # (plus the length of the cheat) closer to the end on the fair path, so:
    # A -> B -> ...cheat... -> Y -> -> Z is a good cheat if B and Y are more
    # than 100 + len(cheat) steps apart and len(cheat) < 20
    for pos in fair_path:
        possible_cheats = {
            (pos[0] + i, pos[1] + j)
            for i in range(-19, 20)
            for j in range(-19, 20)
            if abs(i) + abs(j) < 20
            and 0 < pos[0] + i < height
            and 0 < pos[1] + j < width
        }
        possible_cheats -= walls

        good_cheats = 0
        for cheatpos in possible_cheats:
            print("trying ")
            cheat_path_len = dfs(pos, cheatpos, 19)
            # TODO: dfs is bad here, we want the shortest possible cheat route
            # between pos and cheatpos, so bfs would be better here?
            if not cheat_path_len:
                continue
            print(pos, cheatpos, cheat_path_len)
