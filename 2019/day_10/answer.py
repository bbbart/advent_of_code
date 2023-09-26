from collections import defaultdict
from itertools import combinations
from math import atan2, gcd, pi, sqrt


# pylint: disable=too-many-branches,too-many-locals
def p1(data, is_sample):
    coords = set()
    for row, line in enumerate(data):
        for col, loc in enumerate(line):
            if loc == "#":
                coords.add((col, row))

    see_count = defaultdict(int)

    for a, b in combinations(coords, 2):
        gcd_abs = gcd(abs(a[0] - b[0]), abs(a[1] - b[1]))

        if gcd_abs == 1:
            see_count[a] += 1
            see_count[b] += 1
            continue

        dir_x = (b[0] - a[0]) / gcd_abs
        dir_y = (b[1] - a[1]) / gcd_abs
        if dir_x == 0 or dir_y == 0:
            gcd_abs = 1

        steps = 1
        while True:
            looking_at = (a[0] + steps * dir_x, a[1] + steps * dir_y)

            if looking_at == b:  # I can see you!
                see_count[a] += 1
                see_count[b] += 1
                break

            if looking_at in coords:  # I'm seeing someone else
                break

            steps += 1

    best_loc = max(see_count, key=see_count.get)
    return best_loc, see_count[best_loc]


def angle_from_y_axis(co):
    """Get the angle from the positive y-axis to reach the given coordinate."""
    return (pi / 2 - atan2(co[1], co[0])) % (2 * pi)


def p2(data, is_sample):
    coords = set()
    for row, line in enumerate(data):
        for col, loc in enumerate(line):
            if loc == "#":
                co = (col, row)
                coords.add(co)

    # find best position
    best_loc, _ = p1(data, is_sample)
    coords.remove(best_loc)

    # get the angles of the coordinates with the 'best position' as origin
    new_coords: dict[float, set[tuple]] = defaultdict(set)
    for co in coords:
        new_co = co[0] - best_loc[0], best_loc[1] - co[1]
        angle = angle_from_y_axis(new_co)
        new_coords[angle].add(co)

    # start shooting
    count = 0
    while True:
        for angle, cos in sorted(new_coords.items()):
            shot = sorted(
                cos,
                key=lambda c: sqrt(
                    (c[0] - best_loc[0]) ** 2 + (c[1] - best_loc[1]) ** 2
                ),
            )[0]
            count += 1
            if count == 200:
                return shot[0] * 100 + shot[1]
            cos.remove(shot)
