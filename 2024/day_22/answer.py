#!/usr/bin/env python

from collections import deque
from itertools import islice, pairwise


def p1(data: list[str], is_sample: bool):
    codes = set(map(int, data))

    def prng(seed):
        secret = seed
        while True:
            # step one
            res = secret << 6  #  multiply by 64
            secret ^= res  # XOR
            secret &= 16777215  # mod 16777216

            # step two
            res = secret >> 5  # floor divide by 32
            secret ^= res  # XOR
            secret &= 16777215  # mod 16777216

            # step three
            res = secret << 11  # multiply by 2048
            secret ^= res  # XOR
            secret &= 16777215  # mod 16777216

            yield secret

    total = 0
    for code in codes:
        rng = prng(code)
        total += next(islice(rng, 1999, 2000))

    return total


def p2(data: list[str], is_sample: bool):
    codes = set(map(int, data))

    def prng(seed):
        secret = seed
        for _ in range(2001):
            yield secret

            # step one
            res = secret << 6  #  multiply by 64
            secret ^= res  # XOR
            secret &= 16777215  # mod 16777216

            # step two
            res = secret >> 5  # floor divide by 32
            secret ^= res  # XOR
            secret &= 16777215  # mod 16777216

            # step three
            res = secret << 11  # multiply by 2048
            secret ^= res  # XOR
            secret &= 16777215  # mod 16777216

    prices_per_code = {}
    for code in codes:
        rng = prng(code)
        differences = deque([], 4)
        prices: dict[tuple[int], int] = {}
        for pr1, pr2 in pairwise(rng):
            pr1 %= 10
            pr2 %= 10
            differences.append(pr2 - pr1)
            fixed_diff = tuple(differences)
            if fixed_diff not in prices and len(fixed_diff) == 4:
                prices[fixed_diff] = pr2
        prices_per_code[code] = prices

    possible_differences = set()
    for prices in prices_per_code.values():
        possible_differences.update(prices.keys())

    max_bananas = 0
    for differences in possible_differences:
        max_bananas = max(
            max_bananas,
            sum(
                prices.get(differences, 0)
                for prices in prices_per_code.values()
            ),
        )

    return max_bananas
