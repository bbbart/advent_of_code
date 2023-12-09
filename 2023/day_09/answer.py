#!/usr/bin/env python

from functools import reduce

def predict_next(ints: tuple[int]) -> int:
    last_digits = [ints[-1]]
    differences = [ints[i + 1] - ints[i] for i in range(len(ints) - 1)]
    while any(differences):
        differences = [ints[i + 1] - ints[i] for i in range(len(ints) - 1)]
        ints = differences
        last_digits.append(differences[-1])

    return sum(last_digits)

def predict_previous(ints: tuple[int]) -> int:
    first_digits = [ints[0]]
    differences = [ints[i + 1] - ints[i] for i in range(len(ints) - 1)]
    while any(differences):
        differences = [ints[i + 1] - ints[i] for i in range(len(ints) - 1)]
        ints = differences
        first_digits.append(differences[0])

    return reduce(lambda x, y: y-x, reversed(first_digits))

def p1(data, is_sample):
    total_prediction = 0
    for line in data:
        total_prediction += predict_next(tuple(map(int, line.split())))

    return total_prediction


def p2(data, is_sample):
    total_prediction = 0
    for line in data:
        total_prediction += predict_previous(tuple(map(int, line.split())))

    return total_prediction
