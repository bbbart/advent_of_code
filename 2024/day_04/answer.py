#!/usr/bin/env python

from collections import defaultdict, namedtuple, Counter

coordinate = namedtuple("cooordinate", "x y")


def p1(data: list[str], is_sample: bool):
    letterlocs = defaultdict(list)
    directions = {
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    }

    y = 0
    for line in data:
        x = 0
        for char in line:
            letterlocs[char].append(coordinate(x, y))
            x += 1
        y += 1

    look_for = "XMAS"
    word_count = 0
    for start_loc in letterlocs[look_for[0]]:
        for direction in directions:
            look_at = start_loc
            for letter in look_for[1:]:
                look_at = coordinate(
                    look_at.x + direction[0], look_at.y + direction[1]
                )
                if look_at not in letterlocs[letter]:
                    break
            else:
                word_count += 1

    return word_count


def p2(data: list[str], is_sample: bool):
    letterlocs = defaultdict(list)

    y = 0
    for line in data:
        x = 0
        for char in line:
            letterlocs[char].append(coordinate(x, y))
            x += 1
        y += 1

    width = x
    height = y

    word_count = 0
    for a_loc in letterlocs["A"]:
        if set(a_loc) & set((0, width - 1, height - 1)):
            # 'A' cannot be on the border of the grid
            continue
        if Counter([
            data[a_loc.y + delta_y][a_loc.x + delta_x]
            for delta_x in (-1, 1)
            for delta_y in (-1, 1)
            ]) != {'M': 2, 'S': 2}:
            # corners should contain exactly two 'M' and two 'S
            continue
        if (
            data[a_loc.y - 1][a_loc.x - 1] == data[a_loc.y + 1][a_loc.x + 1]
            or data[a_loc.y - 1][a_loc.x + 1] == data[a_loc.y + 1][a_loc.x - 1]
        ):
            # opposite corners cannot be the same
            continue
        print(a_loc)
        word_count += 1

    return word_count
