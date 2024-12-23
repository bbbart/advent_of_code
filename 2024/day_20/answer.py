#!/usr/bin/env python

from collections import Counter, defaultdict, deque
from itertools import combinations


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
    if is_sample:
        cutoff = 50
    else:
        cutoff = 100

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

    def shortest_path():
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

        path = []
        prev_pos = (x, y)
        path.append(prev_pos)
        while (prev_pos := prev.get(prev_pos)) != start_pos:
            path.append(prev_pos)

        return [start_pos] + list(reversed(path)) + [end_pos]

    fair_path = shortest_path()

    def find_cheat(start, target, max_length):
        dist = defaultdict(lambda: float("inf"))
        prev = {}
        to_visit = walls.copy()
        to_visit.add(start)
        to_visit.add(target)

        dist[start] = 0
        while to_visit:
            x, y = min(to_visit, key=dist.__getitem__)
            to_visit.remove((x, y))
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in to_visit:
                    continue
                if dist[(nx, ny)] < dist[(x, y)] + 1:
                    continue
                dist[(nx, ny)] = dist[(x, y)] + 1
                if dist[(nx, ny)] > max_length:
                    continue
                prev[(nx, ny)] = (x, y)
                if (nx, ny) == target:
                    return dist[(nx, ny)]

    # stategy: for each cell on the fair path, figure out if there is another
    # cell we can reach only by passing to max 19 walls that is more than 100
    # (plus the length of the cheat) closer to the end on the fair path, so:
    # A -> B -> ...cheat... -> Y -> -> Z is a good cheat if B and Y are more
    # than 100 + len(cheat) steps apart and len(cheat) < 20

    # for cheat_start in fair_path:
    #     possible_cheats = {
    #         (cheat_start[0] + i, cheat_start[1] + j)
    #         for i in range(-20, 21)
    #         for j in range(-20, 21)
    #         if abs(i) + abs(j) <= 20
    #         and 0 < cheat_start[0] + i < height
    #         and 0 < cheat_start[1] + j < width
    #         and (cheat_start[0] + i, cheat_start[1] + j) not in walls
    #         and fair_path.index(cheat_start)
    #         - fair_path.index((cheat_start[0] + i, cheat_start[1] + j))
    #         > 1
    #     }

    #     good_cheats = 0
    #     for cheat_end in possible_cheats:
    #         max_gain = fair_path.index(cheat_start) - fair_path.index(cheat_end) + 1
    #         if max_gain < cutoff:
    #             continue
    #         print(f"trying {cheat_start} - {cheat_end}", end="\r")
    #         cheat_path_len = find_cheat(cheat_start, cheat_end, max_gain)
    #         if not cheat_path_len:
    #             continue
    #         print(cheat_start, cheat_end, cheat_path_len)
    #         good_cheats += 1

    def shortest_cheat(start, end, maxlen):
        queue = deque([(start, 0)])
        visited = set()
        while queue:
            pos, dist = queue.popleft()
            if dist > maxlen:
                continue
            if pos == end:
                return dist
            visited.add(pos)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = pos[0] + dx, pos[1] + dy
                # if nx == 0 or ny == 0 or nx == height or ny == width:
                #     continue
                if (nx, ny) not in walls and (nx, ny) != end:
                    continue
                if (nx, ny) not in visited and (
                    (nx, ny),
                    dist + 1,
                ) not in queue:
                    queue.append(((nx, ny), dist + 1))

        return False

    gains = []
    for i in range(len(fair_path) - 1):
        for j in range(i + cutoff, len(fair_path)):
            cheat_start = fair_path[i]
            cheat_end = fair_path[j]
            if (
                abs(cheat_end[0] - cheat_start[0])
                + abs(cheat_end[1] - cheat_start[1])
                > 20
            ):
                continue
            cheat_len = shortest_cheat(cheat_start, cheat_end, 20)
            if not cheat_len:
                continue
            fair_len = i + len(fair_path) - 1 - j
            gain = len(fair_path) - 1 - fair_len - cheat_len
            if gain >= cutoff:
                # print(cheat_start, cheat_end, cheat_len, gain)
                gains.append(gain)

    return len(gains)
