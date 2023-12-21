#!/usr/bin/env python

from collections import deque
from functools import cache


def p1(data, is_sample):
    garden_plots = set()
    starting_pos = None
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                continue
            if char == "S":
                starting_pos = (x, y)
            garden_plots.add((x, y))

    garden = {}
    for co in garden_plots:
        neighbours = {
            (nx, ny)
            for nx, ny in (
                (co[0] - 1, co[1]),
                (co[0] + 1, co[1]),
                (co[0], co[1] - 1),
                (co[0], co[1] + 1),
            )
            if (nx, ny) in garden_plots
        }
        garden[co] = neighbours

    targets = {starting_pos}
    for _ in range(64):
        new_targets = set().union(*(garden[t] for t in targets))
        targets = new_targets

    return len(targets)


def p2(data, is_sample):
    if not is_sample:
        return "N/A"

    garden_plots = set()
    starting_pos = None
    x, y = 0, 0
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                continue
            if char == "S":
                starting_pos = (x, y)
            garden_plots.add((x, y))

    map_width = x + 1
    map_height = y + 1

    @cache
    def get_directions(loc: tuple[int, int]) -> set[tuple[int, int]]:
        """All directions accessible from the given locations."""
        return {
            (dx, dy)
            for dx, dy in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            )
            if ((loc[0] + dx) % map_width, (loc[1] + dy) % map_height)
            in garden_plots
        }

    def bfs_reachable_positions(start, steps):
        # after entering a new `repetition` of the map, after a certain number
        # of steps, that portion enters into an endless cycle of reachable
        # fields, with a period of two. This means that we should be able to
        # simply count the number of map repetitions we have reached and
        # consider them as a single unit, flip-flopping between two values.

        visited = set()
        queue = deque([(start, steps)])

        while queue:
            current_position, steps_remaining = queue.popleft()
            if (current_position, steps_remaining % 2) in visited:
                continue

            visited.add((current_position, steps_remaining % 2))

            if steps_remaining == 0:
                continue

            for directions in get_directions(
                (
                    current_position[0] % map_width,
                    current_position[1] % map_height,
                )
            ):
                queue.append(
                    (
                        (
                            current_position[0] + directions[0],
                            current_position[1] + directions[1],
                        ),
                        steps_remaining - 1,
                    )
                )

        unique_positions = set(
            pos for pos, remaining in visited if remaining == 0
        )
        return unique_positions

    total_steps = 2000  # 26501365  # 26501365 = 481843 * 11 * 5

    reachable_positions = bfs_reachable_positions(starting_pos, total_steps)
    return len(reachable_positions)
