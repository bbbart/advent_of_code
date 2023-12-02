#!/usr/bin/env python

import re


def p1(data, is_sample):
    re_first_digit = re.compile(r"^[a-zA-Z]*(\d)")
    total = 0
    for line in data:
        first_digit = re_first_digit.match(line).groups()[0]
        last_digit = re_first_digit.match(line[::-1]).groups()[0]
        calibration_value = int(first_digit + last_digit)
        total += calibration_value
    return total


def p2(data, is_sample):
    total = 0
    numberwords = (
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    )
    re_numberword = re.compile("|".join(numberwords))
    for line in data:
        partial_word = ""
        for char in line:
            if char.isdigit():
                first_digit = int(char)
                break
            partial_word += char
            first_digit_match = re_numberword.search(partial_word)
            if first_digit_match:
                first_digit = numberwords.index(first_digit_match.group(0))
                break

        partial_word = ""
        for char in reversed(line):
            if char.isdigit():
                last_digit = int(char)
                break
            partial_word = char + partial_word
            last_digit_match = re_numberword.search(partial_word)
            if last_digit_match:
                last_digit = numberwords.index(last_digit_match.group(0))
                break

        calibration_value = 10 * first_digit + last_digit
        total += calibration_value

    return total
