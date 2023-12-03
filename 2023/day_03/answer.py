#!/usr/bin/env python

from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Number:
    numberstring: str
    coordinates: set[tuple[int, int]]

    @property
    def number(self):
        return int(self.numberstring)

    def is_adjacent_to(self, coordinate: tuple[int, int]):
        for co in self.coordinates:
            if (
                abs(co[0] - coordinate[0]) < 2
                and abs(co[1] - coordinate[1]) < 2
            ):
                return True
        return False


def p1(data, is_sample):
    symbol_locations: set[tuple[int, int]] = set()
    numbers: list[Number] = []
    x, y = 0, 0

    for line in data:
        current_number = None
        for char in line:
            if char.isdigit():
                if not current_number:
                    current_number = Number(char, {(x, y)})
                    numbers.append(current_number)
                else:
                    current_number.numberstring += char
                    current_number.coordinates.add((x, y))
            elif char == ".":
                current_number = None
            else:
                symbol_locations.add((x, y))
                current_number = None
            x += 1
        x = 0
        y += 1
        current_number = None

    sum_part_numbers = 0
    for symbol in symbol_locations:
        for number in numbers:
            if number.is_adjacent_to(symbol):
                sum_part_numbers += number.number

    return sum_part_numbers


def p2(data, is_sample):
    possible_gear_locations: set[tuple[int, int]] = set()
    numbers: list[Number] = []
    x, y = 0, 0

    for line in data:
        current_number = None
        for char in line:
            if char.isdigit():
                if not current_number:
                    current_number = Number(char, {(x, y)})
                    numbers.append(current_number)
                else:
                    current_number.numberstring += char
                    current_number.coordinates.add((x, y))
            elif char == ".":
                current_number = None
            elif char == "*":
                possible_gear_locations.add((x, y))
                current_number = None
            x += 1
        x = 0
        y += 1
        current_number = None

    sum_gear_ratios = 0
    for possible_gear in possible_gear_locations:
        adjacent_numbers: list[Number] = []
        for number in numbers:
            if number.is_adjacent_to(possible_gear):
                adjacent_numbers.append(number)
        if len(adjacent_numbers) == 2:
            sum_gear_ratios += (
                adjacent_numbers[0].number * adjacent_numbers[1].number
            )

    return sum_gear_ratios
