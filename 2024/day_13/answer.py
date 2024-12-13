#!/usr/bin/env python

import re
from dataclasses import dataclass


@dataclass
class Machine:
    A: tuple[int]
    B: tuple[int]
    P: tuple[int]


def p1(data: list[str], is_sample: bool):
    machines = []
    for line in data:
        if match := re.match(r"Button A: X\+(\d+), Y\+(\d+)", line):
            button_a = tuple(map(int, match.groups()))
            continue
        if match := re.match(r"Button B: X\+(\d+), Y\+(\d+)", line):
            button_b = tuple(map(int, match.groups()))
            continue
        if match := re.match(r"Prize: X=(\d+), Y=(\d+)", line):
            prize = tuple(map(int, match.groups()))
            continue
        machines.append(Machine(button_a, button_b, prize))
    machines.append(Machine(button_a, button_b, prize))

    tokens = 0
    for m in machines:
        # PX = AX*a + BX*b and PY = AY*a + BY*b
        b = (m.P[1] / m.B[1] - m.A[1] / m.B[1] * m.P[0] / m.A[0]) / (
            1 - m.A[1] / m.B[1] * m.B[0] / m.A[0]
        )
        br = round(b)
        a = (m.P[0] - m.B[0] * br) / m.A[0]
        ar = round(a)
        if (
            m.A[0] * ar + m.B[0] * br == m.P[0]
            and m.A[1] * ar + m.B[1] * br == m.P[1]
        ):
            tokens += 3 * a + b

    return int(tokens)


def p2(data: list[str], is_sample: bool):
    correction = 10_000_000_000_000
    machines = []
    for line in data:
        if match := re.match(r"Button A: X\+(\d+), Y\+(\d+)", line):
            button_a = tuple(map(int, match.groups()))
            continue
        if match := re.match(r"Button B: X\+(\d+), Y\+(\d+)", line):
            button_b = tuple(map(int, match.groups()))
            continue
        if match := re.match(r"Prize: X=(\d+), Y=(\d+)", line):
            prize = tuple(map(int, match.groups()))
            continue
        machines.append(
            Machine(
                button_a,
                button_b,
                (prize[0] + correction, prize[1] + correction),
            )
        )
    machines.append(
        Machine(
            button_a, button_b, (prize[0] + correction, prize[1] + correction)
        )
    )

    tokens = 0
    for m in machines:
        # PX = AX*a + BX*b and PY = AY*a + BY*b
        b = (m.P[1] / m.B[1] - m.A[1] / m.B[1] * m.P[0] / m.A[0]) / (
            1 - m.A[1] / m.B[1] * m.B[0] / m.A[0]
        )
        br = round(b)
        a = (m.P[0] - m.B[0] * br) / m.A[0]
        ar = round(a)
        if (
            m.A[0] * ar + m.B[0] * br == m.P[0]
            and m.A[1] * ar + m.B[1] * br == m.P[1]
        ):
            tokens += 3 * a + b

    return int(tokens)
