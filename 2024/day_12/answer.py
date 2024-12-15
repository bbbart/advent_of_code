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


def p2(data: list[str], is_sample: bool):
    if not is_sample:
        return "N/A"
    return "N/A"

    # # 1/ find shapes as before (shape = set of coordinates)
    # farm: dict[tuple[int], chr] = {}
    # for y, line in enumerate(data):
    #     for x, char in enumerate(line):
    #         farm[(x, y)] = char

    # seen: set[tuple[int]] = set()
    # fields: list[set[tuple[int]]] = []

    # steps = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    # while seen != set(farm.keys()):
    #     start = (set(farm.keys()) - seen).pop()
    #     crop = farm[start]

    #     to_explore: set[tuple[int]] = set()
    #     to_explore.add(start)

    #     field = set()
    #     while to_explore:
    #         x, y = to_explore.pop()
    #         seen.add((x, y))
    #         field.add((x, y))
    #         for dx, dy in steps:
    #             if (x + dx, y + dy) in field:
    #                 continue
    #             if farm.get((x + dx, y + dy), None) == crop:
    #                 to_explore.add((x + dx, y + dy))
    #     fields.append(field)

    # # 2/ traverse the boundary clockwise and count the corners
    # # the code below doesn't make sense
    # price = 0
    # for field in fields:
    #     boundary = {
    #         cell
    #         for cell in field
    #         if any(
    #             (cell[0] + step[0], cell[1] + step[1]) not in field
    #             for step in steps
    #         )
    #     }

    #     edges = 0

    #     for x, y in boundary:
    #         for step in steps:
    #             nx, ny = x + step[0], y + step[1]
    #             if (nx, ny) not in boundary:
    #                 edges += 1

    #     print(f"area: {len(field)}, sides: {edges}")
    #     price += len(field) * edges

    # return price
