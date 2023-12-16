#!/usr/bin/env python

from collections import defaultdict, deque, namedtuple
from time import sleep

beamhead: tuple[tuple[int, int], chr] = namedtuple("beamhead", ("loc", "dir"))
deltas = {"u": (0, -1), "r": (1, 0), "d": (0, 1), "l": (-1, 0)}
bends = {
    "/": {"u": "r", "r": "u", "d": "l", "l": "d"},
    "\\": {"u": "l", "r": "d", "d": "r", "l": "u"},
}
splits = {"-": ("l", "r"), "|": ("u", "d")}


def show_contraption(
    contraption: dict, energized: set, width: int, height: int
):
    print("\033c\033[3J", end="")
    sleep(0.125)
    for y in range(height):
        for x in range(width):
            if (x, y) in energized:
                print("#", end="")
                continue

            for char, locs in contraption.items():
                if (x, y) in locs:
                    print(char, end="")
                    break
        print()


def p1(data, is_sample):
    contraption: dict[chr, list[tuple[int, int]]] = defaultdict(list)

    x, y = 0, 0
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            contraption[char].append((x, y))

    width = x + 1
    height = y + 1

    energized: set[tuple[int, int]] = set()

    beamheads = deque([beamhead((-1, 0), "r")])
    beamheads_archive = set()

    while beamheads:
        # show_contraption(contraption, energized, width, height)
        b = beamheads.pop()

        nextloc = tuple(x + y for x, y in zip(b.loc, deltas[b.dir]))
        if not (0 <= nextloc[0] < width and 0 <= nextloc[1] < height):
            continue

        energized.add(nextloc)
        beamheads_archive.add(b)

        if nextloc in contraption["."]:
            newbeamhead = beamhead(nextloc, b.dir)
            if newbeamhead not in beamheads_archive:
                beamheads.append(newbeamhead)
        elif nextloc in contraption["/"]:
            newdir = bends['/'][b.dir]
            newbeamhead = beamhead(nextloc, newdir)
            if newbeamhead not in beamheads_archive:
                beamheads.append(newbeamhead)
        elif nextloc in contraption["\\"]:
            newdir = bends['\\'][b.dir]
            newbeamhead = beamhead(nextloc, newdir)
            if newbeamhead not in beamheads_archive:
                beamheads.append(newbeamhead)
        elif nextloc in contraption["-"]:
            if b.dir in splits['-']:
                newbeamhead = beamhead(nextloc, b.dir)
                if newbeamhead not in beamheads_archive:
                    beamheads.append(newbeamhead)
            else:
                for newdir in splits['-']:
                    newbeamhead = beamhead(nextloc, newdir)
                    if newbeamhead not in beamheads_archive:
                        beamheads.append(newbeamhead)
        elif nextloc in contraption["|"]:
            if b.dir in splits["|"]:
                newbeamhead = beamhead(nextloc, b.dir)
                if newbeamhead not in beamheads_archive:
                    beamheads.append(newbeamhead)
            else:
                for newdir in splits['|']:
                    newbeamhead = beamhead(nextloc, newdir)
                    if newbeamhead not in beamheads_archive:
                        beamheads.append(newbeamhead)

    return len(energized)


def p2(data, is_sample):
    contraption: dict[tuple[int, int], chr] = {}

    x, y = 0, 0
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char != ".":
                contraption[(x, y)] = char
    width = x + 1
    height = y + 1

    def energize(bh: beamhead) -> set[tuple[int, int]]:
        seen.add(bh)
        nextloc = tuple(x + y for x, y in zip(bh.loc, deltas[bh.dir]))

        newly_energized = set()

        # pass through empty space or aligned splitters
        # no need for recursion here
        while (
            (nextloc not in contraption)
            or (contraption[nextloc] == "-" and bh.dir in ("l", "r"))
            or (contraption[nextloc] == "|" and bh.dir in ("u", "d"))
        ):
            if not (0 <= nextloc[0] < width and 0 <= nextloc[1] < height):
                # we reached an edge of the contraption
                return newly_energized

            newly_energized.add(nextloc)
            nextloc = tuple(x + y for x, y in zip(nextloc, deltas[bh.dir]))

        newly_energized.add(nextloc)

        # we hit a mirror
        if contraption[nextloc] in ("/", "\\"):
            newdir = bends[contraption[nextloc]][bh.dir]
            newbeamhead = beamhead(nextloc, newdir)
            if not newbeamhead in seen:
                newly_energized |= energize(newbeamhead)
        # we hit an orthogonal splitter
        elif contraption[nextloc] in ('-', '|'):
            for newdir in splits[contraption[nextloc]]:
                newbeamhead = beamhead(nextloc, newdir)
                if not newbeamhead in seen:
                    newly_energized |= energize(newbeamhead)

        return newly_energized

    maxencount = 0
    for start_y in range(-1, height):
        for start_x, start_dir in ((-1, "r"), (width, "l")):
            startbh = beamhead((start_x, start_y), start_dir)
            seen = set()
            maxencount = max(maxencount, len(energize(startbh)))
    for start_x in range(-1, width):
        for start_y, start_dir in ((-1, "d"), (height, "u")):
            startbh = beamhead((start_x, start_y), start_dir)
            seen = set()
            maxencount = max(maxencount, len(energize(startbh)))
    return maxencount
