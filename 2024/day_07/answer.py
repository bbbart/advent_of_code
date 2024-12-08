#!/usr/bin/env python

from itertools import accumulate, product
from operator import add, mul


def p1(data: list[str], is_sample: bool):
    OPERATORS = (add, mul)

    calib_total = 0
    for line in data:
        result, values = line.split(": ")
        result = int(result)
        values = tuple(map(int, values.split(" ")))

        for ops in product(OPERATORS, repeat=len(values) - 1):
            ops = iter(ops)

            def op(x, y):
                nonlocal ops
                operator = next(ops)  # pylint: disable=cell-var-from-loop
                return operator(x, y)

            total = 0
            for total in accumulate(values, op):
                if total > result:
                    break
            else:
                if total == result:
                    calib_total += result
                    break

    return calib_total


def p2(data: list[str], is_sample: bool):
    OPERATORS = (add, mul, lambda x, y: x * 10**len(str(y)) + y)

    calib_total = 0
    for line in data:
        result, values = line.split(": ")
        result = int(result)
        values = tuple(map(int, values.split(" ")))

        for ops in product(OPERATORS, repeat=len(values) - 1):
            ops = iter(ops)

            def op(x, y):
                nonlocal ops
                operator = next(ops)  # pylint: disable=cell-var-from-loop
                return operator(x, y)

            total = 0
            for total in accumulate(values, op):
                if total > result:
                    break
            else:
                if total == result:
                    calib_total += result
                    break

    return calib_total
