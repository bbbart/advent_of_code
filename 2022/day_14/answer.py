from collections import namedtuple
from enum import Enum
from itertools import chain, pairwise
from warnings import warn

Coordinate = namedtuple("Coordinate", ("x", "y"))


class Space(Enum):
    AIR = "."
    ROCK = "#"
    SOURCE = "+"
    SAND = "o"

    def __str__(self):
        return self.value


class Cave:
    def __init__(self, width, height, min_x):
        self.min_x = min_x
        self._cave = [[Space.AIR for _ in range(width)] for _ in range(height)]
        self._sand_source_co = None

    def __str__(self):
        cave_as_str = ""
        for line in self._cave:
            cave_as_str += ("".join(map(str, line))) + "\n"
        return cave_as_str

    @property
    def width(self):
        return len(self._cave[0])

    @property
    def height(self):
        return len(self._cave)

    @property
    def sand_source_co(self):
        return self._sand_source_co

    @sand_source_co.setter
    def sand_source_co(self, co: Coordinate):
        self._sand_source_co = co
        self.set_at_co(co, Space.SOURCE)

    def get_at_co(self, co: Coordinate):
        real_x = co.x - self.min_x
        if real_x < 0:
            raise IndexError
        return self._cave[co.y][real_x]

    def set_at_co(self, co: Coordinate, space: Space):
        real_x = co.x - self.min_x
        if real_x < 0:
            raise IndexError
        self._cave[co.y][real_x] = space

    def drop_sand(self, source=None):
        if not source:
            source = self.sand_source_co

        if not source:
            warn("Trying to drop sand in a cave without sand source.")
            return False

        try:
            x = source.x
            y = source.y + 1
            while self.get_at_co(Coordinate(x, y)) == Space.AIR:
                y += 1

            if self.get_at_co(Coordinate(x - 1, y)) == Space.AIR:
                return self.drop_sand(source=Coordinate(x - 1, y))
            if self.get_at_co(Coordinate(x + 1, y)) == Space.AIR:
                return self.drop_sand(source=Coordinate(x + 1, y))
            self.set_at_co(Coordinate(x, y - 1), Space.SAND)

            return True
        except IndexError:
            return False


class CaveWithFloor(Cave):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the floor
        self._cave.append([Space.AIR for _ in range(self.width)])
        self._cave.append([Space.ROCK for _ in range(self.width)])

    def get_at_co(self, co: Coordinate):
        if co.y == self.height - 1:
            return Space.ROCK

        real_x = co.x - self.min_x
        if real_x < 0 or real_x >= self.width:
            return Space.AIR

        return self._cave[co.y][real_x]

    def set_at_co(self, co: Coordinate, space: Space):
        real_x = co.x - self.min_x
        if real_x < 0:
            self.expand(direction="left", spaces=abs(real_x))
            real_x = 0

        if real_x > self.width - 1:
            self.expand(direction="right", spaces=real_x - self.width + 1)

        self._cave[co.y][real_x] = space

    def expand(self, direction="right", spaces=1):
        for _ in range(spaces):
            if direction == "left":
                for line in self._cave[:-1]:
                    line.insert(0, Space.AIR)
                self._cave[-1].insert(0, Space.ROCK)
                self.min_x -= 1
            else:
                for line in self._cave[:-1]:
                    line.append(Space.AIR)
                self._cave[-1].append(Space.ROCK)


# pylint: disable=too-many-locals
# I'm sorry...
def create_cave(data, caveclass=Cave):
    paths = []
    for line in data:
        coordinates = []
        for point in line.split(" -> "):
            x, y = map(int, point.split(","))
            coordinates.append(Coordinate(x, y))
        paths.append(coordinates)

    cave_left_edge_x = min(co.x for co in chain(*paths))
    cave_right_edge_x = max(co.x for co in chain(*paths))
    cave_depth_y = max(co.y for co in chain(*paths))
    cave = caveclass(
        cave_right_edge_x - cave_left_edge_x + 1,
        cave_depth_y + 1,
        cave_left_edge_x,
    )

    # set source
    cave.sand_source_co = Coordinate(500, 0)

    # set rock paths
    for path in paths:
        for co_from, co_to in pairwise(path):
            if co_from.x == co_to.x:
                for y in range(
                    min(co_from.y, co_to.y), max(co_from.y, co_to.y) + 1
                ):
                    cave.set_at_co(Coordinate(co_from.x, y), Space.ROCK)
            elif co_from.y == co_to.y:
                for x in range(
                    min(co_from.x, co_to.x), max(co_from.x, co_to.x) + 1
                ):
                    cave.set_at_co(Coordinate(x, co_from.y), Space.ROCK)
            else:
                warn("Trying to trace a diagonal rock path?")

    return cave


def p1(data, is_sample):
    cave = create_cave(data)

    count = 0
    while cave.drop_sand():
        count += 1

    return count


def p2(data, is_sample):
    cave = create_cave(data, CaveWithFloor)

    count = 0
    while cave.drop_sand():
        count += 1
        if cave.get_at_co(cave.sand_source_co) == Space.SAND:
            break

    if cave.get_at_co(cave.sand_source_co) != Space.SAND:
        warn("Sand dropping simulation stopped before blocking the source!")

    return count
