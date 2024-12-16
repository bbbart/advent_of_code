#!/usr/bin/env python


# pylint: disable=too-many-locals
def p1(data: list[str], is_sample: bool):
    farm: dict[tuple[int], chr] = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            farm[(x, y)] = char

    in_fields: set[tuple[int]] = set()

    steps = set(((0, 1), (0, -1), (1, 0), (-1, 0)))
    price = 0
    while in_fields != set(farm.keys()):
        area = 0
        peri = 0
        to_explore: set[tuple[int]] = set()

        start = (set(farm.keys()) - in_fields).pop()
        crop = farm[start]
        to_explore.add(start)
        explored = set()
        while to_explore:
            x, y = to_explore.pop()
            in_fields.add((x, y))
            explored.add((x, y))
            area += 1
            for dx, dy in steps:
                if (x + dx, y + dy) in explored:
                    continue
                if farm.get((x + dx, y + dy), None) == crop:
                    to_explore.add((x + dx, y + dy))
                else:
                    peri += 1
        price += area * peri

    return price


# pylint: disable=too-many-branches,too-many-statements
def p2(data: list[str], is_sample: bool):
    # this is a naive implementation of the solution discussed in
    # https://www.youtube.com/watch?v=fwEUDQBTPKM

    # 1/ find shapes as before (shape = set of coordinates)
    farm: dict[tuple[int], chr] = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            farm[(x, y)] = char

    seen: set[tuple[int]] = set()
    fields: list[set[tuple[int]]] = []

    steps = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    while seen != set(farm.keys()):
        start = (set(farm.keys()) - seen).pop()
        crop = farm[start]

        to_explore: set[tuple[int]] = set()
        to_explore.add(start)

        field = set()
        while to_explore:
            x, y = to_explore.pop()
            seen.add((x, y))
            field.add((x, y))
            for dx, dy in steps:
                if (x + dx, y + dy) in field:
                    continue
                if farm.get((x + dx, y + dy), None) == crop:
                    to_explore.add((x + dx, y + dy))
        fields.append(field)

    # 2/ find the number of edges of each field
    price = 0
    for field in fields:
        # scan up
        edges_north = 0
        scanned_up = set()
        for x, y in field:
            # find nearest edge upwards
            if (x, y) in scanned_up:
                continue
            scanned_up.add((x, y))
            while True:
                y -= 1
                if (x, y) in field:
                    if (x, y) in scanned_up:
                        at_edge = False
                        break
                    scanned_up.add((x, y))
                else:
                    at_edge = True
                    edges_north += 1
                    y += 1
                    break
            while at_edge:
                x -= 1
                if (x, y) in field and (x, y - 1) not in field:
                    scanned_up.add((x, y))
                else:
                    x += 1
                    break
            while at_edge:
                x += 1
                if (x, y) in field and (x, y - 1) not in field:
                    scanned_up.add((x, y))
                else:
                    x -= 1
                    break
        # scan down
        edges_south = 0
        scanned_down = set()
        for x, y in field:
            # find nearest edge downwards
            if (x, y) in scanned_down:
                continue
            scanned_down.add((x, y))
            while True:
                y += 1
                if (x, y) in field:
                    if (x, y) in scanned_down:
                        at_edge = False
                        break
                    scanned_down.add((x, y))
                else:
                    at_edge = True
                    edges_south += 1
                    y -= 1
                    break
            while at_edge:
                x -= 1
                if (x, y) in field and (x, y + 1) not in field:
                    scanned_down.add((x, y))
                else:
                    x += 1
                    break
            while at_edge:
                x += 1
                if (x, y) in field and (x, y + 1) not in field:
                    scanned_down.add((x, y))
                else:
                    x -= 1
                    break
        # scan left
        edges_west = 0
        scanned_left = set()
        for x, y in field:
            # find nearest edge leftwards
            if (x, y) in scanned_left:
                continue
            scanned_left.add((x, y))
            while True:
                x -= 1
                if (x, y) in field:
                    if (x, y) in scanned_left:
                        at_edge = False
                        break
                    scanned_left.add((x, y))
                else:
                    at_edge = True
                    edges_west += 1
                    x += 1
                    break
            while at_edge:
                y -= 1
                if (x, y) in field and (x - 1, y) not in field:
                    scanned_left.add((x, y))
                else:
                    y += 1
                    break
            while at_edge:
                y += 1
                if (x, y) in field and (x - 1, y) not in field:
                    scanned_left.add((x, y))
                else:
                    y -= 1
                    break
        # scan right
        edges_east = 0
        scanned_right = set()
        for x, y in field:
            # find nearest edge rightwards
            if (x, y) in scanned_right:
                continue
            scanned_right.add((x, y))
            while True:
                x += 1
                if (x, y) in field:
                    if (x, y) in scanned_right:
                        at_edge = False
                        break
                    scanned_right.add((x, y))
                else:
                    at_edge = True
                    edges_east += 1
                    x -= 1
                    break
            while at_edge:
                y -= 1
                if (x, y) in field and (x + 1, y) not in field:
                    scanned_right.add((x, y))
                else:
                    y += 1
                    break
            while at_edge:
                y += 1
                if (x, y) in field and (x + 1, y) not in field:
                    scanned_right.add((x, y))
                else:
                    y -= 1
                    break
        price += len(field) * (
            edges_north + edges_south + edges_west + edges_east
        )

    return price
