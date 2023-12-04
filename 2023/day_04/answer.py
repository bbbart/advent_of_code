#!/usr/bin/env python

import re


def parse_card(numbers: list[int | str]) -> int:
    winning_numbers = set()
    card_numbers = set()

    store_in = winning_numbers
    for number in numbers[1:]:
        if number == "|":
            store_in = card_numbers
            continue
        store_in.add(number)

    number_of_winners = len(card_numbers & winning_numbers)
    return number_of_winners


def p1(data, is_sample):
    total_score = 0

    for line in data:
        numbers = re.findall(r"\d+|\|", line)
        number_of_winners = parse_card(numbers)
        if number_of_winners:
            total_score += 2 ** (number_of_winners - 1)

    return total_score


def p2(data, is_sample):
    # stores card id as key and number of winners as value
    cards: dict[int, int] = {}
    for line in data:
        numbers = re.findall(r"\d+|\|", line)
        cards[int(numbers[0])] = parse_card(numbers)

    # stores card id as key and number of copies as value
    card_counts: dict[int, int] = {cid: 1 for cid in cards}
    for card_id, number_of_winners in cards.items():
        for i in range(card_id + 1, card_id + 1 + number_of_winners):
            try:
                card_counts[i] += card_counts[card_id]
            except KeyError:
                break

    return sum(cc for cc in card_counts.values())
