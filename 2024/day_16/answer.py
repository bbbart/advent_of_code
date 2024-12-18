#!/usr/bin/env python

# pylint: disable=too-many-locals
def p1(data: list[str], is_sample: bool):
    # parse the input data
    grid: dict[tuple[int], chr] = {}
    start_pos = None
    target_pos = None
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            if char == "S":
                start_pos = (x, y)
            elif char == "E":
                target_pos = (x, y)

    directions = set(((1, 0), (0, 1), (-1, 0), (0, -1)))

    # modified dijkstra
    # this is slooooooooooooooooooowwww
    # but it works :-)
    to_explore = {
        ((x, y), orientation)
        for (x, y), char in grid.items()
        if char != "#"
        for orientation in directions
    }
    distances = {pos: float("inf") for pos in to_explore}

    begin = (start_pos, (1, 0))
    distances[begin] = 0

    while to_explore:
        pos = min(to_explore, key=distances.__getitem__)
        to_explore.remove(pos)
        for dx, dy in directions:
            if (pos[1][0] + dx, pos[1][1] + dy) == (0, 0):
                # we don't reverse
                continue
            new_pos = ((pos[0][0] + dx, pos[0][1] + dy), (dx, dy))
            points = 1 if (dx, dy) == pos[1] else 1001
            new_distance = distances[pos] + points
            if new_pos in to_explore:
                distances[new_pos] = min(new_distance, distances[new_pos])

    return min(
        distance for pos, distance in distances.items() if pos[0] == target_pos
    )


def p2(data: list[str], is_sample: bool):
    # tried brute forcing, but that took way too long
    return 'N/A'
