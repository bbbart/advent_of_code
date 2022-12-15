#!/usr/bin/env python

from string import ascii_lowercase, ascii_uppercase

priority_order = ascii_lowercase + ascii_uppercase


def get_priority(letter):
    return priority_order.index(letter) + 1


def p1(data, is_sample):
    total_priority = 0
    for rucksack in data:
        comp1 = set(rucksack[0 : len(rucksack) // 2])
        comp2 = set(rucksack[len(rucksack) // 2 :])
        common = comp1.intersection(comp2).pop()
        total_priority += get_priority(common)

    return total_priority


def p2(data, is_sample):
    total_badge_priority = 0
    for group in zip(*[iter(data)] * 3):
        rucksack1 = set(group[0])
        rucksack2 = set(group[1])
        rucksack3 = set(group[2])
        badge = rucksack1.intersection(rucksack2).intersection(rucksack3).pop()
        total_badge_priority += get_priority(badge)

    return total_badge_priority
