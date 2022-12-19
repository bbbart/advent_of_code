from dataclasses import dataclass


@dataclass
class CubePosition:
    x: int
    y: int
    z: int

    def is_adjacent(self, other):
        return (
            abs(self.x - other.x),
            abs(self.y - other.y),
            abs(self.z - other.z),
        ) in ((0, 0, 1), (0, 1, 0), (1, 0, 0))


def parse_input(data):
    for line in data:
        yield CubePosition(*map(int, line.split(",")))


def p1(data, is_sample):
    cubes = tuple(parse_input(data))
    surface_area = 0
    for cube in cubes:
        freefaces = 6
        for othercube in cubes:
            if cube.is_adjacent(othercube):
                freefaces -= 1
        surface_area += freefaces

    return surface_area
