#!/usr/bin/env python

from collections import defaultdict


def p1(data: list[str], is_sample: bool):
    towels = tuple(data[0].split(", "))
    patterns = set(data[2:])

    # recursive function
    def pattern_possible(pattern, towels):
        if pattern in towels:
            return True

        for i in range(1, len(pattern)):
            if pattern[:i] not in towels:
                continue
            if pattern_possible(pattern[i:], towels):
                break
        else:
            return False
        return True

    return sum(pattern_possible(pattern, towels) for pattern in patterns)


def p2(data: list[str], is_sample: bool):
    towels = set(data[0].split(", "))
    patterns = set(data[2:])

    total = 0
    # dynamic programming
    for pattern in patterns:
        n = len(pattern)
        dp = defaultdict(int)
        dp[0] = 1

        for i in range(1, n + 1):
            for j in range(i):
                if pattern[j:i] in towels:
                    dp[i] += dp[j]

        total += dp[n]

    return total
