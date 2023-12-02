#!/usr/bin/env python

import re
from collections import defaultdict
from functools import reduce


class ImpossibleGame(Exception):
    pass


def p1(data, is_sample):
    cube_totals = {"red": 12, "green": 13, "blue": 14}
    possible_game_total = 0
    for line in data:
        game_id = int(line.split()[1][:-1])
        grabs = line.split(":")[1].split(";")
        try:
            for grab in grabs:
                for colour, amount in cube_totals.items():
                    num_revealed = re.search(rf"(\d+) {colour}", grab)
                    if not num_revealed:
                        continue
                    if int(num_revealed.group(1)) > amount:
                        raise ImpossibleGame
        except ImpossibleGame:
            continue

        possible_game_total += game_id

    return possible_game_total


def p2(data, is_sample):
    re_grab_data = re.compile(r"^(?P<amount>\d+) (?P<colour>.+)$")
    total_power = 0
    for line in data:
        cube_minimums = defaultdict(int)
        grabs = line.split(":")[1].split(";")
        for grab in grabs:
            for grab_info in grab.split(","):
                grab_data = re_grab_data.match(grab_info.strip())
                current_min = cube_minimums[grab_data["colour"]]
                cube_minimums[grab_data["colour"]] = max(
                    current_min, int(grab_data["amount"])
                )
        game_power = reduce(lambda x, y: x * y, cube_minimums.values())
        total_power += game_power

    return total_power
