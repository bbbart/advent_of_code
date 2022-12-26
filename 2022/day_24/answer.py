from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import count
from math import lcm
from warnings import warn


class ExpeditionDied(Exception):
    pass


class ExpeditionEscaped(Exception):
    pass


class Directions(Enum):
    RIGHT = auto()
    DOWN = auto()
    WAIT = auto()
    LEFT = auto()
    UP = auto()


@dataclass
class Co:
    x: int
    y: int

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return f"{self.x},{self.y}"


@dataclass
class Blizzard:
    pos: Co
    orientation: chr
    id_: int = field(default_factory=count().__next__)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return self.orientation + str(self.pos)

    def move(self, walls: set[Co], boundaries: tuple[int]):
        min_x, max_x, min_y, max_y = boundaries
        if self.orientation == "^":
            self.pos.y -= 1
            if self.pos in walls:
                self.pos.y = max_y
        elif self.orientation == ">":
            self.pos.x += 1
            if self.pos in walls:
                self.pos.x = min_x
        elif self.orientation == "v":
            self.pos.y += 1
            if self.pos in walls:
                self.pos.y = min_y
        elif self.orientation == "<":
            self.pos.x -= 1
            if self.pos in walls:
                self.pos.x = max_x


@dataclass
class Valley:
    walls: set[Co]
    blizzards: set[Blizzard]
    entrance: Co
    exit_: Co

    def __post_init__(self):
        min_x: int = min((wall.x for wall in self.walls))
        max_x: int = max((wall.x for wall in self.walls))
        min_y: int = min((wall.y for wall in self.walls))
        max_y: int = max((wall.y for wall in self.walls))
        self.boundaries = (min_x + 1, max_x - 1, min_y + 1, max_y - 1)
        self.expedition: Co = deepcopy(self.entrance)
        self.max_blizzard_states = lcm(max_x - min_x - 1, max_y - min_y - 1)

    def __hash__(self):
        return hash(
            ";".join([str(b) for b in self.blizzards] + [str(self.expedition)])
        )

    def is_outside(self, co: Co):
        return not (
            self.boundaries[0] <= co.x <= self.boundaries[1]
            and self.boundaries[2] <= co.y <= self.boundaries[3]
        ) and not co in (self.entrance, self.exit_)

    def move_blizzards(self):
        for blizzard in self.blizzards:
            blizzard.move(self.walls, self.boundaries)

    def _move_expedition(self, decision: Directions):
        if decision == Directions.UP:
            self.expedition.y -= 1
        elif decision == Directions.RIGHT:
            self.expedition.x += 1
        elif decision == Directions.DOWN:
            self.expedition.y += 1
        elif decision == Directions.LEFT:
            self.expedition.x -= 1
        elif decision == Directions.WAIT:
            pass
        else:
            warn(f"Unknown decision made by expedition: {decision}")

        if self.expedition in {b.pos for b in self.blizzards}:
            raise ExpeditionDied("blizzard")
        if self.expedition in self.walls or self.is_outside(self.expedition):
            raise ExpeditionDied("wall")
        if self.expedition == self.exit_:
            raise ExpeditionEscaped

    def step(self, decision: Directions):
        self.move_blizzards()
        self._move_expedition(decision)

    @property
    def distance_from_exit(self):
        return abs(self.exit_.y - self.expedition.y) + abs(
            self.exit_.x - self.expedition.x
        )

    def show(self):
        for y in range(self.boundaries[2] - 1, self.boundaries[3] + 2):
            for x in range(self.boundaries[0] - 1, self.boundaries[1] + 2):
                pos = Co(x, y)
                if pos in self.walls:
                    print("#", end="")
                    continue
                if pos == self.expedition:
                    print("E", end="")
                    continue
                local_blizzards = [
                    b.orientation for b in self.blizzards if b.pos == pos
                ]
                if len(local_blizzards) == 0:
                    print(".", end="")
                elif len(local_blizzards) == 1:
                    print(local_blizzards[0], end="")
                else:
                    print(len(local_blizzards), end="")
            print()


def show_path(path: list[Directions], end: str = None):
    print("".join(p.name[0] for p in path), end=end)


def parse_data(data):
    walls: set(Co) = set()
    blizzards: set[Blizzard] = set()
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == ".":
                if row == 0:
                    start_pos = Co(col, row)
                elif row == len(data) - 1:
                    finish_pos = Co(col, row)
                else:
                    continue
            elif char == "#":
                walls.add(Co(col, row))
            elif char in ("^", ">", "v", "<"):
                blizzards.add(Blizzard(Co(col, row), char))
            else:
                warn(f"Unknown map character {char}")

    my_pos = start_pos
    return Valley(walls, blizzards, my_pos, finish_pos)


def p1(data, is_sample):
    valley = parse_data(data)

    no_exit: set[tuple[Directions]] = set()
    dejavu: dict[int, tuple(Directions)] = {}
    max_pathlen: list[int] = [1000]  # wild guess

    def walk(valley: Valley, next_step: Directions, path: list[Directions]):
        path.append(next_step)
        # there are three stop conditions:
        #   1/ taking the next step kills the expedition
        try:
            if valley.distance_from_exit > max_pathlen[-1] - len(path):
                raise ExpeditionDied("exhaustion")

            valley.step(next_step)
        except ExpeditionDied:
            no_exit.add(tuple(path))
        except ExpeditionEscaped:
            #   2/ taking the next step leads us through the exit
            max_pathlen.append(len(path))
            return len(path)

        #   3/ taking the next step brings us in a situation we were in before
        if hash(valley) in dejavu:
            alternative_path = dejavu[hash(valley)]
            if alternative_path in no_exit:
                no_exit.add(tuple(path))
                return max_pathlen[-1] + 1

            # now we know that from this position, there is an exit
            # possibility, and that we can do it faster than the one we
            # found earlier. however, we didn't remember the one from
            # before (nor the length of the path), so we just find it again
            # -> here is room for more optimisation
            if len(path) >= len(alternative_path):
                return max_pathlen[-1] + 1
            dejavu[hash(valley)] = path

        if tuple(path) in no_exit:
            return max_pathlen[-1] + 1

        dejavu[hash(valley)] = tuple(path)

        explorations: set[int] = set()
        for d in Directions:
            pathlen = walk(deepcopy(valley), d, deepcopy(path))
            explorations.add(pathlen)
        return min(explorations)

    pathlen = walk(valley, Directions.DOWN, [])
    return pathlen


def solve(
    valley,
    search_order: tuple[Directions],
    max_pathlen=1000,
    dejavu=None,
    no_exit=None,
):

    no_exit: set[tuple[Directions]] = no_exit or set()
    dejavu: dict[int, tuple(Directions)] = dejavu or {}
    max_pathlen: list[int] = [max_pathlen]

    def walk(valley: Valley, next_step: Directions, path: list[Directions]):
        path.append(next_step)
        # there are three stop conditions:
        #   1/ taking the next step kills the expedition
        try:
            if valley.distance_from_exit > max_pathlen[-1] - len(path):
                raise ExpeditionDied("exhaustion")

            valley.step(next_step)
        except ExpeditionDied:
            no_exit.add(tuple(path))
        except ExpeditionEscaped:
            #   2/ taking the next step leads us through the exit
            max_pathlen.append(len(path))
            show_path(path)
            return len(path)

        #   3/ taking the next step brings us in a situation we were in before
        if hash(valley) in dejavu:
            alternative_path = dejavu[hash(valley)]
            if alternative_path in no_exit:
                no_exit.add(tuple(path))
                return max_pathlen[0] + 1

            # now we know that from this position, there is an exit
            # possibility, and that we can do it faster than the one we
            # found earlier. however, we didn't remember the one from
            # before (nor the length of the path), so we just find it again
            # -> here is room for more optimisation
            if len(path) >= len(alternative_path):
                return max_pathlen[0] + 1
            dejavu[hash(valley)] = tuple(path)

        if tuple(path) in no_exit:
            return max_pathlen[0] + 1

        dejavu[hash(valley)] = tuple(path)

        explorations: set[int] = set()
        for d in Directions:
            pathlen = walk(deepcopy(valley), d, deepcopy(path))
            explorations.add(pathlen)
        return min(explorations)

    explorations: set[int] = set()
    for d in Directions:
        pathlen = walk(deepcopy(valley), d, [])
        explorations.add(pathlen)
    return min(explorations), dejavu, no_exit


def p2(data, is_sample):
    valley = parse_data(data)

    # start to exit
    search_order = (
        Directions.RIGHT,
        Directions.DOWN,
        Directions.WAIT,
        Directions.UP,
        Directions.LEFT,
    )
    timespent1, dejavu, no_exit = solve(
        deepcopy(valley),
        search_order,
        max_pathlen=25 if is_sample else 270,
    )

    # exit to start
    for _ in range(timespent1):
        valley.move_blizzards()
    valley.exit_, valley.entrance = valley.entrance, valley.exit_
    valley.expedition = deepcopy(valley.entrance)
    timespent2, _, _ = solve(
        deepcopy(valley),
        tuple(reversed(search_order)),
        max_pathlen=25 if is_sample else 350,
    )

    # start to exit
    for _ in range(timespent2):
        valley.move_blizzards()
    valley.exit_, valley.entrance = valley.entrance, valley.exit_
    valley.expedition = deepcopy(valley.entrance)
    timespent3, _, _ = solve(
        deepcopy(valley),
        search_order,
        max_pathlen=25 if is_sample else 350,
        dejavu=dejavu,
        no_exit=no_exit,
    )

    return timespent1 + timespent2 + timespent3
