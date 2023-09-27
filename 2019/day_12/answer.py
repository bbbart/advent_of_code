import math
import re
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Moon:
    pos_x: int
    pos_y: int
    pos_z: int
    vel_x: int = 0
    vel_y: int = 0
    vel_z: int = 0

    def move(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.pos_z += self.vel_z

    @property
    def pot(self):
        return abs(self.pos_x) + abs(self.pos_y) + abs(self.pos_z)

    @property
    def kin(self):
        return abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z)

    @property
    def total_energy(self):
        return self.pot * self.kin

    @property
    def state(self):
        return (
            self.pos_x,
            self.pos_y,
            self.pos_z,
            self.vel_x,
            self.vel_y,
            self.vel_z,
        )

    @property
    def pos(self):
        return [self.pos_x, self.pos_y, self.pos_z]

    @property
    def vel(self):
        return [self.vel_x, self.vel_y, self.vel_z]


def p1(data, is_sample):
    coordinates = re.compile(r".=(-?\d+)")

    moons: list[Moon] = []
    for line in data:
        moons.append(Moon(*map(int, coordinates.findall(line))))

    steps = 0
    while steps < 1000:
        # GRAVITY
        for m, n in combinations(moons, 2):
            if m.pos_x < n.pos_x:
                m.vel_x += 1
                n.vel_x -= 1
            elif m.pos_x > n.pos_x:
                m.vel_x -= 1
                n.vel_x += 1

            if m.pos_y < n.pos_y:
                m.vel_y += 1
                n.vel_y -= 1
            elif m.pos_y > n.pos_y:
                m.vel_y -= 1
                n.vel_y += 1

            if m.pos_z < n.pos_z:
                m.vel_z += 1
                n.vel_z -= 1
            elif m.pos_z > n.pos_z:
                m.vel_z -= 1
                n.vel_z += 1

        # VELOCITY
        for m in moons:
            m.move()

        # ENERGY
        energy = sum(m.total_energy for m in moons)

        steps += 1

    return energy


# pylint: disable=too-many-branches
def p2(data, is_sample):
    coordinates = re.compile(r".=(-?\d+)")

    moons: list[Moon] = []
    for line in data:
        moon = Moon(*map(int, coordinates.findall(line)))
        moons.append(moon)

    orig_pos = [
        [m.pos_x for m in moons],
        [m.pos_y for m in moons],
        [m.pos_z for m in moons],
    ]

    periods = [None, None, None]
    steps = 0
    while True:
        # GRAVITY
        for m, n in combinations(moons, 2):
            if m.pos_x < n.pos_x:
                m.vel_x += 1
                n.vel_x -= 1
            elif m.pos_x > n.pos_x:
                m.vel_x -= 1
                n.vel_x += 1

            if m.pos_y < n.pos_y:
                m.vel_y += 1
                n.vel_y -= 1
            elif m.pos_y > n.pos_y:
                m.vel_y -= 1
                n.vel_y += 1

            if m.pos_z < n.pos_z:
                m.vel_z += 1
                n.vel_z -= 1
            elif m.pos_z > n.pos_z:
                m.vel_z -= 1
                n.vel_z += 1

        # VELOCITY
        for m in moons:
            m.move()

        steps += 1

        for i, p in enumerate(periods):
            if not p:
                if [m.pos[i] for m in moons] == orig_pos[i]:
                    periods[i] = steps + 1

        if all(periods):
            return math.lcm(*periods)
