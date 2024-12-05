#!/usr/bin/env python

import re
from collections import defaultdict


def page_class(rules):

    class Page(int):
        def __lt__(self, other):
            return other in rules[self]

    return Page


def parse_data(data: list[str]) -> (dict[int, list[int]], list[list['Page']]):
    rules = defaultdict(list)
    updates = []

    for line in data:
        rule = re.match(r"^(?P<before>\d+)\|(?P<after>\d+)$", line)
        if rule:
            rules[int(rule.group("before"))].append(int(rule.group("after")))
            continue

        if not line:
            Page = page_class(rules)
            continue

        updates.append(list(map(Page, line.split(","))))

    return rules, updates


def p1(data: list[str], is_sample: bool):
    _, updates = parse_data(data)

    total = 0
    for update in updates:
        if sorted(update) == update:
            total += update[len(update) // 2]

    return total


def p2(data: list[str], is_sample: bool):
    _, updates = parse_data(data)

    total = 0
    for update in updates:
        update_sorted = sorted(update)
        if update_sorted != update:
            total += update_sorted[len(update_sorted) // 2]

    return total
