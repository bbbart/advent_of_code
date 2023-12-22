#!/usr/bin/env python

from collections import namedtuple
from functools import cache
from itertools import chain, dropwhile, product, takewhile
from queue import Empty, PriorityQueue

Cell = namedtuple("Cell", ("xy", "block_id"))


def populate_cells_and_blocks(data, cells, fallingblocks) -> set:
    for line in data:
        ends = tuple(
            map(lambda s: tuple(map(int, s.split(","))), line.split("~"))
        )

        # we store all the cell coordinates as z, y, x so we can easily sort
        # them on positional height
        # also, within a block, the cells are stored from low to high
        block = tuple(
            sorted(
                product(
                    range(min(e[2] for e in ends), max(e[2] for e in ends) + 1),
                    range(min(e[1] for e in ends), max(e[1] for e in ends) + 1),
                    range(min(e[0] for e in ends), max(e[0] for e in ends) + 1),
                )
            )
        )
        fallingblocks.put_nowait(block)
        cells |= set(block)

    return cells, fallingblocks


def drop_blocks(fallingblocks, cells) -> list:
    supportedblocks = []
    while True:
        try:
            block = fallingblocks.get_nowait()
        except Empty:
            break

        if any(z == 1 for z, _, _ in block):
            # we're on the floor
            supportedblocks.append(tuple(block))
            continue
        if (cells - set(block)) & set((z - 1, y, x) for (z, y, x) in block):
            supportedblocks.append(tuple(block))
            continue

        cells -= set(block)
        block = tuple((c[0] - 1, c[1], c[2]) for c in block)
        cells |= set(block)
        fallingblocks.put(block)

    return supportedblocks


def p1(data, is_sample):
    cells: set[tuple[int, int, int]] = set()
    fallingblocks: PriorityQueue = PriorityQueue()

    populate_cells_and_blocks(data, cells, fallingblocks)

    supportedblocks = sorted(drop_blocks(fallingblocks, cells))

    @cache
    def immediately_supported_by(disiblocks: tuple) -> set:
        isb = set()
        disicells = set(disiblocks)
        max_disiz = max(z for z, _, _ in disicells)
        for other in takewhile(
            lambda o: o[0][0] == max_disiz + 1,
            dropwhile(lambda o: o[0][0] <= max_disiz, supportedblocks),
        ):
            if any(z == 1 for z, _, _ in other):
                # we're on the floor
                continue
            if not (cells - disicells - set(other)) & set(
                (z - 1, y, x) for (z, y, x) in other
            ):
                # we would fall without disiblocks
                isb.add(other)

        return isb

    return len(
        set(b for b in supportedblocks if not immediately_supported_by(b))
    )


def p2(data, is_sample):
    # this works for the sample input, but yields the wrong answer for the
    # actual input (too low). I don't understand why however...
    if not is_sample:
        return 'N/A'

    cells: set[tuple[int, int, int]] = set()
    fallingblocks: PriorityQueue = PriorityQueue()

    populate_cells_and_blocks(data, cells, fallingblocks)
    supportedblocks = sorted(drop_blocks(fallingblocks, cells))

    @cache
    def immediately_supported_by(disiblocks: tuple[tuple]) -> set:
        isb = set()
        disicells = set(chain(*disiblocks))
        max_disiz = max(z for z, _, _ in disicells)
        for other in takewhile(
            lambda o: o[0][0] == max_disiz + 1,
            dropwhile(lambda o: o[0][0] <= max_disiz, supportedblocks),
        ):
            if any(z == 1 for z, _, _ in other):
                # we're on the floor
                continue
            if not (cells - disicells - set(other)) & set(
                (z - 1, y, x) for (z, y, x) in other
            ):
                # we would fall without disiblocks
                isb.add(other)

        return isb

    ans = 0
    counter = 0
    for block in reversed(supportedblocks):
        falling = {block}
        while falling:
            falling = immediately_supported_by(tuple(falling))
            ans += len(falling)
        counter += 1

    return ans
