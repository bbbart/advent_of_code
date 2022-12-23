from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass, field

Co = namedtuple("Co", ("x", "y"))


@dataclass
class Screen:
    width: int
    height: int
    lit_pixels: set[Co] = field(default_factory=set)

    def show(self):
        for y in range(self.height):
            for x in range(self.width):
                if Co(x, y) in self.lit_pixels:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def rect(self, width: int, height: int):
        for x in range(width):
            for y in range(height):
                self.lit_pixels.add(Co(x, y))

    def rot_row(self, row, by):
        to_add = set()
        to_remove = set()
        for co in deepcopy(self.lit_pixels):
            if co.y != row:
                continue
            to_remove.add(co)
            to_add.add(Co((co.x + by) % self.width, co.y))

        self.lit_pixels -= to_remove
        self.lit_pixels ^= to_add

    def rot_col(self, col, by):
        to_add = set()
        to_remove = set()
        for co in deepcopy(self.lit_pixels):
            if co.x != col:
                continue
            to_remove.add(co)
            to_add.add(Co(co.x, (co.y + by) % self.height))

        self.lit_pixels -= to_remove
        self.lit_pixels ^= to_add


def run_commands(data, screen: Screen):
    for command in data:
        commands = command.split()
        if commands[0] == "rect":
            screen.rect(*map(int, commands[1].split("x")))
        elif commands[0] == "rotate":
            by = int(commands[-1])
            if commands[1] == "row":
                row = int(commands[2].lstrip("y="))
                screen.rot_row(row, by)
            elif commands[1] == "column":
                col = int(commands[2].lstrip("x="))
                screen.rot_col(col, by)


def p1(data, is_sample):
    if is_sample:
        screen = Screen(7, 3)
    else:
        screen = Screen(50, 6)

    run_commands(data, screen)

    return len(screen.lit_pixels)


def p2(data, is_sample):
    if is_sample:
        screen = Screen(7, 3)
    else:
        screen = Screen(50, 6)

    run_commands(data, screen)

    screen.show()
