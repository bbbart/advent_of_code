from collections import namedtuple
from copy import deepcopy
from warnings import warn

Co = namedtuple("Co", ("x", "y"))


def rectangle(elves: set[Co]) -> tuple[Co]:
    elf = elves.pop()
    min_x, max_x, min_y, max_y = elf.x, elf.x, elf.y, elf.y
    elves.add(elf)
    for elf in elves:
        min_x = min(min_x, elf.x)
        max_x = max(max_x, elf.x)
        min_y = min(min_y, elf.y)
        max_y = max(max_y, elf.y)

    return (Co(min_x, min_y), Co(max_x, max_y))


def show_elves(elves):
    rect = rectangle(elves)
    for y in range(rect[0].y, rect[1].y + 1):
        for x in range(rect[0].x, rect[1].x + 1):
            if Co(x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()


def shift_direction_order(direction_order: list[str]):
    direction_order.append(direction_order.pop(0))


def do_i_want_to_go(elf, elves):
    for co in (
        Co(elf.x - 1, elf.y - 1),
        Co(elf.x, elf.y - 1),
        Co(elf.x + 1, elf.y - 1),
        Co(elf.x - 1, elf.y + 1),
        Co(elf.x, elf.y + 1),
        Co(elf.x + 1, elf.y + 1),
        Co(elf.x - 1, elf.y),
        Co(elf.x + 1, elf.y),
    ):
        if co in elves:
            return True

    return False


def can_i_go(elf: Co, direction: str, elves: set[Co]) -> bool:
    if direction == "N":
        return not any(
            Co(x, elf.y - 1) in elves for x in range(elf.x - 1, elf.x + 2)
        )
    if direction == "E":
        return not any(
            Co(elf.x + 1, y) in elves for y in range(elf.y - 1, elf.y + 2)
        )
    if direction == "S":
        return not any(
            Co(x, elf.y + 1) in elves for x in range(elf.x - 1, elf.x + 2)
        )
    if direction == "W":
        return not any(
            Co(elf.x - 1, y) in elves for y in range(elf.y - 1, elf.y + 2)
        )

    warn("Unknown direction")
    return False


def consider_and_move(elves: set[Co], direction_order: list[chr]) -> set[Co]:
    # consider
    considerations: dict[Co, Co] = {}
    for elf in elves:
        if not do_i_want_to_go(elf, elves):
            continue
        for direction in direction_order:
            if can_i_go(elf, direction, elves):
                if direction == "N":
                    considerations[elf] = Co(elf.x, elf.y - 1)
                    break
                if direction == "E":
                    considerations[elf] = Co(elf.x + 1, elf.y)
                    break
                if direction == "S":
                    considerations[elf] = Co(elf.x, elf.y + 1)
                    break
                if direction == "W":
                    considerations[elf] = Co(elf.x - 1, elf.y)
                    break

    # move
    targets = list(considerations.values())
    for elf, target in considerations.items():
        if targets.count(target) == 1:
            elves.remove(elf)
            elves.add(target)

    return elves


def init_elves(data) -> set[Co]:
    elves: set[Co] = set()

    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == "#":
                elves.add(Co(col, row))

    return elves


def p1(data, is_sample):
    elves = init_elves(data)
    direction_order = ["N", "S", "W", "E"]

    for _ in range(10):
        consider_and_move(elves, direction_order)
        shift_direction_order(direction_order)

    tl, br = rectangle(elves)
    return (br.x - tl.x + 1) * (br.y - tl.y + 1) - len(elves)


def p2(data, is_sample):
    elves = init_elves(data)
    direction_order = ["N", "S", "W", "E"]

    count = 0
    while True:
        elves_old = deepcopy(elves)
        consider_and_move(elves, direction_order)
        count += 1

        if elves_old == elves:
            break

        shift_direction_order(direction_order)

    return count
