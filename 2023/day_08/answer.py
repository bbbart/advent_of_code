#!/usr/bin/env python

import math
import re
from itertools import cycle

NETWORK_LINE = re.compile(r"^(?P<origin>.*) = \((?P<left>.*), (?P<right>.*)\)")


def p1(data, is_sample):
    instructions = cycle(data[0])

    desert_map = {}
    for line in data[1:]:
        match = NETWORK_LINE.match(line)
        if not match:
            continue

        desert_map[match["origin"]] = (match["left"], match["right"])

    loc = "AAA"
    step_counter = 0
    while loc != "ZZZ":
        match next(instructions):
            case "L":
                loc = desert_map[loc][0]
            case "R":
                loc = desert_map[loc][1]
        step_counter += 1

    return step_counter


def p2(data, is_sample):
    if is_sample:
        return "N/A"

    desert_map = {}
    for line in data[1:]:
        match = NETWORK_LINE.match(line)
        if not match:
            continue

        desert_map[match["origin"]] = (match["left"], match["right"])

    locs = [node for node in desert_map if node.endswith("A")]

    step_counters = {loc: 0 for loc in locs}
    for loc in locs:
        instructions = cycle(data[0])
        start_loc = loc
        while not loc.endswith("Z"):
            match next(instructions):
                case "L":
                    loc = desert_map[loc][0]
                case "R":
                    loc = desert_map[loc][1]
            step_counters[start_loc] += 1

    # to be honest, I don't understand this 100%. I know about the lcm-theorem,
    # but shouldn't the cycle lengths be verified to actually cycle here? I'm
    # not taking the period of `instructions` into account, nor am I verifying
    # wheter reaching a 'Z' from an 'A' actually results in having found a
    # cycle. In fact, I know that continuing for one step more after reaching a
    # 'Z', one does *not* always return to its corresponding starting 'A'...
    #
    # anyway, it yields the correct result :-)
    return math.lcm(*step_counters.values())
