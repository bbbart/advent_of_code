#!/usr/bin/env python


def p1(data: list[str], is_sample: bool):
    left, right = [], []
    for line in data:
        l, r = map(int, line.split("   "))
        left.append(l)
        right.append(r)

    total_distance = 0
    for l, r in zip(sorted(left), sorted(right)):
        total_distance += abs(l - r)

    return total_distance


def p2(data: list[str], is_sample: bool):
    left, right = [], []
    for line in data:
        l, r = map(int, line.split("   "))
        left.append(l)
        right.append(r)

    similarity_score = 0
    for l in left:
        c = right.count(l)
        similarity_score += l*c

    return similarity_score
