#!/usr/bin/env python

import re
from collections import defaultdict, namedtuple
from functools import cache, reduce

re_step = re.compile(r"^(?P<label>.+)(?P<operation>[-=])(?P<focallength>\d*)")
lens = namedtuple("lens", ("label", "focallength"))


@cache
def hasha(ss: str) -> int:
    return reduce(lambda total, c: (total + ord(c)) * 17 % 256, ss, 0)


def p1(data, is_sample):
    initseq = data[0].split(",")

    return sum(hasha(i_s) for i_s in initseq)


def p2(data, is_sample):
    initseq = data[0].split(",")

    lenses = defaultdict(list)
    for step in initseq:
        instructions = re_step.match(step)
        box_num = hasha(instructions["label"])
        if instructions["operation"] == "=":
            new_lens = lens(
                instructions["label"], int(instructions["focallength"])
            )
            for i, l in enumerate(lenses[box_num][:]):
                if l.label == instructions["label"]:
                    lenses[box_num][i] = new_lens
                    break
            else:
                lenses[box_num].append(new_lens)
        else:  # instructions["operation"] == "-":
            for l in lenses[box_num][:]:
                if l.label == instructions["label"]:
                    lenses[box_num].remove(l)
                    break

    total_focusing_power = 0
    for b, l in lenses.items():
        for slot, le in enumerate(l, start=1):
            total_focusing_power += (b + 1) * slot * le.focallength

    return total_focusing_power
