import re
from dataclasses import dataclass
from functools import reduce


class Gap(Exception):
    pass


@dataclass
class Clearing:
    fr: int
    to: int

    def overlaps(self, other):
        return min(self.to, other.to) - max(self.fr, other.fr) >= -1

    def join(self, other):
        if self.overlaps(other):
            return Clearing(min(self.fr, other.fr), max(self.to, other.to))
        raise Gap(min(self.to, other.to), max(self.fr, other.fr))

    def __lt__(self, other):
        return self.fr < other.fr


@dataclass
class Coordinate:
    x: int
    y: int

    def __hash__(self):
        return hash(f"{self.x}{self.y}")

    def distance_to(self, other):
        return abs(other.x - self.x) + abs(self.y - other.y)

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x


@dataclass
class Sensor:
    co: Coordinate
    beacon: Coordinate

    def __post_init__(self):
        self.covering_radius = self.co.distance_to(self.beacon)


def parse_data(data):
    sensors_beacons = {}
    for line in data:
        sx, sy, bx, by = map(
            int,
            re.match(
                r"Sensor at x=(-?\d+), y=(-?\d+): "
                r"closest beacon is at x=(-?\d+), y=(-?\d+)",
                line,
            ).groups(),
        )
        sensors_beacons[Coordinate(sx, sy)] = Coordinate(bx, by)

    return sensors_beacons


def p1(data, is_sample=False):
    sensors_beacons = parse_data(data)

    # determine min_x and max_x to search in the given row
    min_x = min(
        sensor.x - abs(sensor.x - beacon.x)
        for sensor, beacon in sensors_beacons.items()
    )
    max_x = max(
        sensor.x + abs(sensor.x - beacon.x)
        for sensor, beacon in sensors_beacons.items()
    )

    # figure out for every pos in the row if we are nearer to a sensor than
    # it's nearest beacon
    no_beacon = set()
    y = 2000000
    if is_sample:
        y = 10
    for x in range(min_x, max_x + 1):
        co_to_check = Coordinate(x, y)
        if co_to_check in sensors_beacons.values():
            continue

        for sensor, beacon in sensors_beacons.items():
            distance_sb = sensor.distance_to(beacon)
            if sensor.distance_to(co_to_check) <= distance_sb:
                no_beacon.add(co_to_check)

    return len(no_beacon)


# pylint: disable=too-many-locals
# So sorry... :-p
def p2(data, is_sample=False):
    sensors = []
    for co_sensor, co_beacon in parse_data(data).items():
        sensors.append(Sensor(co_sensor, co_beacon))

    min_x, max_x = 0, 4000000
    min_y, max_y = 0, 4000000
    if is_sample:
        max_x = 20
        max_y = 20

    # we're going over the scanning field row by row
    # (as suggested by p1)
    for y in range(min_y, max_y + 1):
        # given there is only one eligible location for our distress
        # signal, we can break the search as soon as we found a coordinate
        # not covered by any of our sensors, so we check the x range of every
        # sensor on our current row
        x_clear = []
        for sensor in sensors:
            distance_y = abs(y - sensor.co.y)
            wiggle_room_x = sensor.covering_radius - distance_y
            if wiggle_room_x < 0:
                continue
            clear_from = max(min_x, sensor.co.x - wiggle_room_x)
            clear_to = min(max_x, sensor.co.x + wiggle_room_x)
            x_clear.append(Clearing(clear_from, clear_to))

        try:
            clearage = reduce(Clearing.join, sorted(x_clear))
            if clearage.fr != min_x:
                raise Gap(min_x, clearage.fr)
            if clearage.to != max_x:
                raise Gap(clearage.to, max_x)
        except Gap as gap:
            assert gap.args[1] - gap.args[0] == 2
            x = gap.args[0] + 1
            return x * 4000000 + y

    return None
