from copy import deepcopy
from dataclasses import dataclass
from itertools import cycle
from warnings import warn


class ReachedBottom(Exception):
    pass


@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)


class Rock:
    def __init__(self, shape: str):
        self._shape = shape
        self._matrix, self.width, self.height = self.__analyze_shape(shape)

    def __str__(self):
        return self._shape

    def falling_shape(self) -> str:
        return self._shape.replace("#", "@")

    def is_solid_at(self, x: int, y: int):
        try:
            return self._matrix[y][x]
        except IndexError:
            return False

    def get_filled_chamber_coordinates(
        self, bottomleft: Coordinate
    ) -> list[Coordinate]:
        for y in range(self.height):
            for x in range(self.width):
                if self.is_solid_at(x, y):
                    yield bottomleft + Coordinate(x, self.height - 1 - y)

    @staticmethod
    def __analyze_shape(shape):
        lines = shape.split("\n")
        width = max(len(line) for line in lines)
        height = len(lines)
        matrix = []
        for line in lines:
            matrix.append([char == "#" for char in line])

        return matrix, width, height


class Chamber:
    def __init__(self, width: int, jetstream):
        self.width = width
        self.__jetstream = jetstream
        self._matrix = []
        self._fallingrock: Rock = None
        self._fallingrock_pos: Coordinate = None

    def __str__(self):
        lines_to_print = []
        falling_coordinates = []
        top_y = 0
        if self._fallingrock:
            falling_coordinates = tuple(
                self._fallingrock.get_filled_chamber_coordinates(
                    self._fallingrock_pos
                )
            )
            top_y = self._fallingrock_pos.y + self._fallingrock.height
        for y in range(max(len(self._matrix), top_y)):
            try:
                line = self._matrix[y]
            except IndexError:
                line = None

            string = "|"
            for x in range(self.width):
                if Coordinate(x, y) in falling_coordinates:
                    string += "@"
                elif line and line[x]:
                    string += "#"
                else:
                    string += "."
            string += "|"
            lines_to_print.insert(0, string)
        lines_to_print.append("+" + self.width * "-" + "+")

        return "\n".join(lines_to_print)

    @property
    def tower_height(self):
        return len(self._matrix)

    def __has_overlap(self, coordinates: list[Coordinate]) -> bool:
        for co in coordinates:
            try:
                if self._matrix[co.y][co.x]:
                    return True
            except IndexError:
                continue

        return False

    def _move_falling_rock(self, direction="v"):
        match direction:
            case "v":
                new_y = self._fallingrock_pos.y - 1
                falling_coordinates = (
                    self._fallingrock.get_filled_chamber_coordinates(
                        Coordinate(self._fallingrock_pos.x, new_y)
                    )
                )
                if new_y < 0 or self.__has_overlap(falling_coordinates):
                    raise ReachedBottom
                self._fallingrock_pos.y = new_y
            case "<":
                new_x = self._fallingrock_pos.x - 1
                falling_coordinates = (
                    self._fallingrock.get_filled_chamber_coordinates(
                        Coordinate(new_x, self._fallingrock_pos.y)
                    )
                )
                if new_x >= 0 and not self.__has_overlap(falling_coordinates):
                    self._fallingrock_pos.x = new_x
            case ">":
                new_x = self._fallingrock_pos.x + 1
                falling_coordinates = (
                    self._fallingrock.get_filled_chamber_coordinates(
                        Coordinate(new_x, self._fallingrock_pos.y)
                    )
                )
                if (
                    new_x + self._fallingrock.width <= self.width
                    and not self.__has_overlap(falling_coordinates)
                ):
                    self._fallingrock_pos.x = new_x
            case _:
                warn(f"Unknown direction to move: {direction}")

    def add_new_rock(self, rock: Rock):
        # get initial position of rock
        # we define the position of rocks as a coordinate pointing to the
        # bottom left corner of the shape matrix
        rock_init_x = 2
        rock_init_y = 3

        # WELCOME THE ROCK
        self._fallingrock = rock
        self._fallingrock_pos = Coordinate(
            rock_init_x, len(self._matrix) + rock_init_y
        )

        # MOVE IT ABOUT UNTIL IT COMES TO REST
        while True:
            try:
                self._move_falling_rock(next(self.__jetstream))
                self._move_falling_rock("v")
            except ReachedBottom:
                self._fallingrock = None
                break

        # STORE IT IN OUR MATRIX
        for _ in range(self._fallingrock_pos.y - len(self._matrix), 0, -1):
            self._matrix.append([False] * self.width)
            warn("Seems the rock is still falling...?")
        matrix_copy = deepcopy(self._matrix)
        for y in range(rock.height - 1, -1, -1):
            try:
                matrix_y = self._fallingrock_pos.y + rock.height - 1 - y
                line = matrix_copy[matrix_y]
                for x in range(self.width - self._fallingrock_pos.x):
                    matrix_x = self._fallingrock_pos.x + x
                    line[matrix_x] = rock.is_solid_at(x, y) or line[matrix_x]
                self._matrix[matrix_y] = line
            except IndexError:
                newline = [False] * self._fallingrock_pos.x
                for x in range(self.width - self._fallingrock_pos.x):
                    newline.append(rock.is_solid_at(x, y))
                self._matrix.append(newline)


def get_rock_cycle():
    return cycle(
        (
            Rock("####"),
            Rock(" # \n###\n # "),
            Rock("  #\n  #\n###"),
            Rock("#\n#\n#\n#"),
            Rock("##\n##"),
        )
    )


def p1(data, is_sample=False):
    jetstream = cycle(data[0])

    chamber = Chamber(7, jetstream)
    rocks = get_rock_cycle()
    for count, rock in enumerate(rocks, start=1):
        chamber.add_new_rock(rock)
        if count == 2022:
            break

    return chamber.tower_height
