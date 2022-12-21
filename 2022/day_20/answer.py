from copy import deepcopy
from dataclasses import dataclass

KEY = 811589153


@dataclass
class Number:
    number: int

    def __post_init__(self):
        self.decrypted_number = self.number * KEY


def p1(data, is_sample):
    numbers = list(map(Number, map(int, data)))

    for number in deepcopy(numbers):
        oldpos = numbers.index(number)
        newpos = (oldpos + number.number) % (len(numbers) - 1)
        del numbers[oldpos]
        numbers.insert(newpos, number)

    numbers = [number.number for number in numbers]
    pos_zero = numbers.index(0)
    coordinates = [
        numbers[(pos_zero + delta) % len(numbers)]
        for delta in (1000, 2000, 3000)
    ]
    return sum(coordinates)


def p2(data, is_sample):
    numbers_orig = list(map(Number, map(int, data)))
    numbers_mixed = deepcopy(numbers_orig)

    def mix(numbers_orig, numbers_mixed):
        for number in numbers_orig:
            oldpos = numbers_mixed.index(number)
            newpos = (oldpos + number.decrypted_number) % (
                len(numbers_mixed) - 1
            )
            del numbers_mixed[oldpos]
            numbers_mixed.insert(newpos, number)
        return numbers_mixed

    for _ in range(10):
        numbers_mixed = mix(numbers_orig, numbers_mixed)

    numbers = [number.number for number in numbers_mixed]
    pos_zero = numbers.index(0)
    coordinates = [
        numbers[(pos_zero + delta) % len(numbers)]
        for delta in (1000, 2000, 3000)
    ]
    return sum(coordinates) * KEY
