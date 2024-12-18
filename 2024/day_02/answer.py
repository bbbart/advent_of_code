#!/usr/bin/env python

from itertools import pairwise


def parse_input(data: list[str]) -> list[list[int]]:
    reports = []
    for levels in data:
        reports.append(tuple(map(int, levels.split())))
    return reports


def p1(data: list[str], is_sample: bool):
    reports = parse_input(data)

    safe_count = 0
    for report in reports:
        increasing = report[0] < report[-1]
        for l1, l2 in pairwise(report):
            if abs(l1 - l2) > 3:
                break
            if increasing and l1 >= l2:
                break
            if not increasing and l1 <= l2:
                break
        else:
            safe_count += 1

    return safe_count


def p2(data: list[str], is_sample: bool):
    reports = parse_input(data)
    safe_count = 0

    def is_safe(report) -> bool:
        increasing = report[0] < report[-1]
        for l1, l2 in pairwise(report):
            if abs(l1 - l2) > 3:
                return False
            if increasing and l1 >= l2:
                return False
            if not increasing and l1 <= l2:
                return False
        return True

    for report in reports:
        if is_safe(report):
            safe_count += 1
        else:
            # very naive approach: we just brute force here, basically we could
            # also try (first) by removing the offending l1 or l2 from above
            for index in range(len(report)):
                if is_safe(report[:index] + report[index + 1 :]):
                    safe_count += 1
                    break

    return safe_count
