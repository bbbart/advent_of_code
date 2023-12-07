#!/usr/bin/env python

from collections import Counter
from dataclasses import dataclass


class UnknownHandType(Exception):
    pass


@dataclass(frozen=True)
class Hand:
    cardstring: str
    card_order: str = "23456789TJQKA"

    @property
    def handtype(self):
        return self._calculate_handtype(self.cardstring)

    def _calculate_handtype(self, cardstring):
        # pylint: disable=too-many-return-statements
        counter = Counter(cardstring)
        if len(counter) == 5:
            return 0  # high card
        if len(counter) == 4:
            return 1  # one pair
        if len(counter) == 3:
            if max(counter.values()) == 2:
                return 2  # two pairs
            if max(counter.values()) == 3:
                return 3  # three of a kind
            raise UnknownHandType(cardstring)
        if len(counter) == 2:
            if max(counter.values()) == 3:
                return 4  # full house
            if max(counter.values()) == 4:
                return 5  # four of a kind
            raise UnknownHandType(cardstring)
        if len(counter) == 1:
            return 6  # five of a kind
        raise UnknownHandType(cardstring)

    def __lt__(self, other):
        if self.cardstring == other.cardstring:
            return True

        if self.handtype != other.handtype:
            return self.handtype < other.handtype

        for selfcard, othercard in zip(self.cardstring, other.cardstring):
            if selfcard != othercard:
                return self.card_order.index(selfcard) < self.card_order.index(
                    othercard
                )

        # this should be unreachable code
        return True


@dataclass(frozen=True)
class Hand2(Hand):
    card_order: str = "J23456789TQKA"

    @property
    def handtype(self):
        # this now calculates the maximum /potential/ type, given that J cards
        # are jokers; it's always more beneficial to replace all Js with all
        # the same cards instead of combinations of different cards (if you
        # consider every possible replacement)
        return max(
            self._calculate_handtype(self.cardstring.replace("J", c))
            for c in self.card_order
        )


def p1(data, is_sample):
    hands = {}
    for line in data:
        cardstring, bid = line.split()
        hands[Hand(cardstring)] = int(bid)

    total_winnings = 0
    for rank, hand in enumerate(sorted(hands), start=1):
        total_winnings += rank * hands[hand]

    return total_winnings


def p2(data, is_sample):
    hands = {}
    for line in data:
        cardstring, bid = line.split()
        hands[Hand2(cardstring)] = int(bid)

    total_winnings = 0
    for rank, hand in enumerate(sorted(hands), start=1):
        total_winnings += rank * hands[hand]

    return total_winnings
