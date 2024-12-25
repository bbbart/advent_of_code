#!/usr/bin/env python


# pylint: disable=too-many-branches
def p1(data: list[str], is_sample: bool):
    locks: set[tuple[int]] = set()
    keys: set[tuple[int]] = set()
    lock_or_key: bool = None
    for line in data:
        if lock_or_key is None and line.count("#") == 5:
            lock_or_key = True
            schema = [0] * 5
            continue
        if lock_or_key is None and line.count(".") == 5:
            lock_or_key = False
            schema = [0] * 5
            continue
        if not line:
            if lock_or_key:
                locks.add(tuple(schema))
            else:
                keys.add(tuple(map(lambda x: 5 - x, schema)))
            lock_or_key = None
            continue
        for pos, char in enumerate(line):
            if lock_or_key and char == "#":
                schema[pos] += 1
            elif not lock_or_key and char == ".":
                schema[pos] += 1
    if lock_or_key:
        locks.add(tuple(schema))
    else:
        keys.add(tuple(map(lambda x: 5 - x, schema)))

    matches = 0
    for lock in locks:
        for key in keys:
            for pins in zip(lock, key):
                if sum(pins) > 5:
                    break
            else:
                matches += 1

    return matches


def p2(data: list[str], is_sample: bool):
    if not is_sample:
        return "N/A"
    return "N/A"
