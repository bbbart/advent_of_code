from dataclasses import dataclass
from warnings import warn


@dataclass
class Coordinate:
    x: int
    y: int

    def move(self, direction: str):
        match direction:
            case "R":
                self.x += 1
            case "L":
                self.x -= 1
            case "U":
                self.y += 1
            case "D":
                self.y -= 1

        if self.x < 0 or self.y < 0:
            warn("negative coordinates")

    def __str__(self):
        return f"({self.x}, {self.y})"


def move_tail(pos_t, pos_h):
    if pos_h.x == pos_t.x:  # H and T are on the same col
        if pos_h.y == pos_t.y:
            # overlapping, so stay here
            return
        if pos_h.y > pos_t.y:
            # same col, so go up
            pos_t.move("U")
        else:
            # same col, so go down
            pos_t.move("D")
    elif pos_h.x < pos_t.x:  # H is more to the left of T
        if pos_h.y == pos_t.y:
            # same row, so go left
            pos_t.move("L")
        elif pos_h.y > pos_t.y:
            # different row, different col, so go diagonally
            pos_t.move("L")
            pos_t.move("U")
        else:
            pos_t.move("L")
            pos_t.move("D")
    else:  # H is more to the right of T
        if pos_h.y == pos_t.y:
            # same row, so go right
            pos_t.move("R")
        elif pos_h.y > pos_t.y:
            # different row, different col, so go diagonally
            pos_t.move("R")
            pos_t.move("U")
        else:
            pos_t.move("R")
            pos_t.move("D")


def touching(pos_t, pos_h):
    return abs(pos_t.x - pos_h.x) <= 1 and abs(pos_t.y - pos_h.y) <= 1


def print_scene(pos_knots):
    for y in range(
        max(pos.y for pos in pos_knots),
        min(pos.y for pos in pos_knots) - 1,
        -1,
    ):
        for x in range(
            min(pos.x for pos in pos_knots),
            max(pos.x for pos in pos_knots) + 1,
        ):
            for index, pos in enumerate(pos_knots):
                if (x, y) == (pos.x, pos.y):
                    print(index, end="")
                    break
            else:
                print(".", end="")
        print()
    print()


def p1(data):
    pos_h = Coordinate(1000, 1000)
    pos_t = Coordinate(1000, 1000)
    pos_t_history = set()

    pos_t_history.add(str(pos_t))
    for instruction in data:
        direction, count = instruction.split()
        for _ in range(int(count)):
            pos_h.move(direction)
            if not touching(pos_t, pos_h):
                move_tail(pos_t, pos_h)
                pos_t_history.add(str(pos_t))
            # print_scene([pos_h, pos_t])

    return len(pos_t_history)


def p2(data):
    pos_knots = [Coordinate(1000, 1000) for _ in range(10)]
    pos_t_history = set()

    pos_t_history.add(str(pos_knots[-1]))
    for instruction in data:
        direction, count = instruction.split()
        for _ in range(int(count)):
            head = pos_knots[0]
            head.move(direction)
            for index in range(len(pos_knots) - 1):
                head = pos_knots[index]
                tail = pos_knots[index + 1]
                if not touching(tail, head):
                    move_tail(tail, head)
            pos_t_history.add(str(pos_knots[-1]))
            # print_scene(pos_knots)

    return len(pos_t_history)
