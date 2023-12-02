import string
from collections import defaultdict, deque
from functools import cache
from itertools import chain


# pylint: disable=too-many-locals
def p1(data, is_sample):
    if not is_sample:
        return "N/A"
    keys = {}
    doors = {}
    entrance = None, None
    passages = set()
    x, y = 0, 0
    for line in data:
        if line == "":
            break
        x = 0
        for char in line:
            match char:
                case "@":
                    entrance = x, y
                case _ if char in string.ascii_lowercase:
                    keys[(x, y)] = char
                case _ if char in string.ascii_uppercase:
                    doors[(x, y)] = char
            if char != "#":
                passages.add((x, y))
            x += 1
        y += 1

    vault: dict[tuple[int], list[tuple[int]]] = defaultdict(list)
    for passage in passages:
        neighbours = set(
            tuple(map(sum, zip(passage, delta)))
            for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        )
        for co in neighbours & passages:
            vault[passage].append(co)

    @cache
    def trace_path(start: tuple, end: tuple, collected_keys: tuple):
        visited = set()
        queue = deque([(start, [start])])

        while queue:
            cur_loc, path = queue.popleft()

            if cur_loc == end:
                return path

            if cur_loc in visited:
                continue

            if cur_loc in doors:
                door = doors[cur_loc]
                if door.lower() not in collected_keys:
                    continue

            visited.add(cur_loc)

            for neighbour in vault.get(cur_loc, []):
                if neighbour not in visited:
                    new_path = path[:] + [neighbour]
                    queue.append((neighbour, new_path))

        return None

    def find_shortest_path(current, remaining, visited, seen):
        if not remaining:
            return 0, []

        if (current, tuple(remaining)) in seen:
            return seen[(current, tuple(remaining))]

        min_distance = len(keys) * len(vault)
        best_path = None

        for next_key in remaining:
            path_to_key = trace_path(
                current, next_key, tuple(keys[v] for v in visited)
            )
            if not path_to_key:
                continue

            distance, path = find_shortest_path(
                next_key, remaining - {next_key}, visited + [next_key], seen
            )

            distance += len(path_to_key) - 1

            if distance < min_distance:
                min_distance = distance
                best_path = [next_key] + path

        seen[(current, tuple(remaining))] = (min_distance, best_path)
        return min_distance, best_path

    # this takes about 30 minutes on my laptop
    distance, _ = find_shortest_path(entrance, set(keys), [], {})
    return distance
