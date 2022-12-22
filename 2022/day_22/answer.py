import re
from collections import namedtuple
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from warnings import warn

Position = namedtuple("Position", ("x", "y"))


@dataclass
class Face:
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def rel2abs(self, pos: Position):
        return Position(pos.x + self.min_x, pos.y + self.min_y)

    def abs2rel(self, pos: Position):
        return Position(pos.x - self.min_x, pos.y - self.min_y)

    def rel_x(self, pos: Position):
        return pos.x - self.min_x

    def rel_y(self, pos: Position):
        return pos.y - self.min_y

    def abs_x(self, pos: Position):
        return pos.x + self.min_x

    def abs_y(self, pos: Position):
        return pos.y + self.min_y


class Tile(Enum):
    NO_TILE = " "
    OPEN = "."
    SOLID = "#"

    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"


DIRECTIONS = (Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH)


def move_p1(current_pos, direction, board, faces, is_sample):
    if direction == Tile.NORTH:
        new_pos = Position(x=current_pos.x, y=(current_pos.y - 1) % len(board))
    elif direction == Tile.EAST:
        new_pos = Position(
            x=(current_pos.x + 1) % len(board[0]), y=current_pos.y
        )
    elif direction == Tile.SOUTH:
        new_pos = Position(x=current_pos.x, y=(current_pos.y + 1) % len(board))
    elif direction == Tile.WEST:
        new_pos = Position(
            x=(current_pos.x - 1) % len(board[0]), y=current_pos.y
        )

    if board[new_pos.y][new_pos.x] == Tile.NO_TILE:
        # no tile, so wrap around
        while True:
            if direction == Tile.NORTH:
                new_pos = Position(x=new_pos.x, y=(new_pos.y + 1) % len(board))
            elif direction == Tile.EAST:
                new_pos = Position(
                    x=(new_pos.x - 1) % len(board[0]), y=new_pos.y
                )
            elif direction == Tile.SOUTH:
                new_pos = Position(x=new_pos.x, y=(new_pos.y - 1) % len(board))
            elif direction == Tile.WEST:
                new_pos = Position(
                    x=(new_pos.x + 1) % len(board[0]), y=new_pos.y
                )

            if board[new_pos.y][new_pos.x] == Tile.NO_TILE:
                new_pos, _ = move_p1(
                    new_pos, direction, board, faces, is_sample
                )
                break

    return new_pos, direction


def face(pos, faces):
    for index, the_face in enumerate(faces, start=1):
        if (
            the_face.min_x <= pos.x <= the_face.max_x
            and the_face.min_y <= pos.y <= the_face.max_y
        ):
            return index
    warn("position not on cube")
    return 0


# pylint: disable=too-many-statements,too-many-branches
# Penalty for hardcoding stuf...
def move_p2(current_pos, direction, board, faces, is_sample):
    if direction == Tile.NORTH:
        new_pos = Position(x=current_pos.x, y=current_pos.y - 1)
    elif direction == Tile.EAST:
        new_pos = Position(x=current_pos.x + 1, y=current_pos.y)
    elif direction == Tile.SOUTH:
        new_pos = Position(x=current_pos.x, y=current_pos.y + 1)
    elif direction == Tile.WEST:
        new_pos = Position(x=current_pos.x - 1, y=current_pos.y)

    change_face = False
    try:
        if board[new_pos.y][new_pos.x] == Tile.NO_TILE:
            change_face = True
    except IndexError:
        change_face = True

    if change_face:
        current_face_id = face(current_pos, faces)
        current_face = faces[current_face_id - 1]
        if is_sample:
            # hardcoding the folding of the sample input
            if current_face_id == 1:
                if direction == Tile.EAST:
                    # walk from 1 to 3
                    target_face = faces[2]
                    direction = Tile.SOUTH
                    new_x = target_face.max_x - current_face.rel_y(current_pos)
                    new_y = target_face.min_y
            elif current_face_id == 2:
                if direction == Tile.SOUTH:
                    # walk from 2 to 6
                    target_face = faces[5]
                    direction = Tile.NORTH
                    new_x = target_face.max_x - current_face.rel_x(current_pos)
                    new_y = target_face.max_y
            elif current_face_id == 4:
                if direction == Tile.NORTH:
                    # walk from 4 to 5
                    target_face = faces[4]
                    direction = Tile.EAST
                    new_x = target_face.min_x
                    new_y = target_face.min_y + current_face.rel_x(current_pos)
            else:
                warn("unknown face change...")
        else:
            # hardcoding the folding of the given input
            if current_face_id == 1:
                if direction == Tile.NORTH:
                    # walk from 1 to 5
                    target_face = faces[4]
                    direction = Tile.EAST
                    new_x = target_face.min_x
                    new_y = target_face.min_y + current_face.rel_x(current_pos)
                elif direction == Tile.WEST:
                    # walk from 1 to 4
                    target_face = faces[3]
                    direction = Tile.EAST
                    new_x = target_face.min_x
                    new_y = target_face.max_y - current_face.rel_y(current_pos)
                else:
                    warn("unknown face change...")
            elif current_face_id == 2:
                if direction == Tile.WEST:
                    # walk from 2 to 4
                    target_face = faces[3]
                    direction = Tile.SOUTH
                    new_x = target_face.min_x + current_face.rel_y(current_pos)
                    new_y = target_face.min_y
                elif direction == Tile.EAST:
                    # walk from 2 to 3
                    target_face = faces[2]
                    direction = Tile.NORTH
                    new_x = target_face.min_x + current_face.rel_y(current_pos)
                    new_y = target_face.max_y
                else:
                    warn("unknown face change...")
            elif current_face_id == 3:
                if direction == Tile.SOUTH:
                    # walk from 3 to 2
                    target_face = faces[1]
                    direction = Tile.WEST
                    new_x = target_face.max_x
                    new_y = target_face.min_y + current_face.rel_x(current_pos)
                elif direction == Tile.EAST:
                    # walk from 3 to 6
                    target_face = faces[5]
                    direction = Tile.WEST
                    new_x = target_face.max_x
                    new_y = target_face.max_y - current_face.rel_y(current_pos)
                elif direction == Tile.NORTH:
                    # walk from 3 to 5
                    target_face = faces[4]
                    direction = Tile.NORTH
                    new_x = target_face.min_x + current_face.rel_x(current_pos)
                    new_y = target_face.max_y
                else:
                    warn("unknown face change...")
            elif current_face_id == 4:
                if direction == Tile.WEST:
                    # walk from 4 to 1
                    target_face = faces[0]
                    direction = Tile.EAST
                    new_x = target_face.min_x
                    new_y = target_face.max_y - current_face.rel_y(current_pos)
                elif direction == Tile.NORTH:
                    # walk from 4 to 2
                    target_face = faces[1]
                    direction = Tile.EAST
                    new_x = target_face.min_x
                    new_y = target_face.min_y + current_face.rel_x(current_pos)
                else:
                    warn("unknown face change...")
            elif current_face_id == 5:
                if direction == Tile.WEST:
                    # walk from 5 to 1
                    target_face = faces[0]
                    direction = Tile.SOUTH
                    new_x = target_face.min_x + current_face.rel_y(current_pos)
                    new_y = target_face.min_y
                elif direction == Tile.SOUTH:
                    # walk from 5 to 3
                    target_face = faces[2]
                    direction = Tile.SOUTH
                    new_x = target_face.min_x + current_face.rel_x(current_pos)
                    new_y = target_face.min_y
                elif direction == Tile.EAST:
                    # walk from 5 to 6
                    target_face = faces[5]
                    direction = Tile.NORTH
                    new_x = target_face.min_x + current_face.rel_y(current_pos)
                    new_y = target_face.max_y
                else:
                    warn("unknown face change...")
            elif current_face_id == 6:
                if direction == Tile.EAST:
                    # walk from 6 to 3
                    target_face = faces[2]
                    direction = Tile.WEST
                    new_x = target_face.max_x
                    new_y = target_face.max_y - current_face.rel_y(current_pos)
                elif direction == Tile.SOUTH:
                    # walk from 6 to 5
                    target_face = faces[4]
                    direction = Tile.WEST
                    new_x = target_face.max_x
                    new_y = target_face.min_y + current_face.rel_x(current_pos)
                else:
                    warn("unknown face change...")

        new_pos = Position(new_x, new_y)

    return new_pos, direction


def show_board(board):
    for line in board:
        for tile in line:
            print(tile.value, end="")
        print()


# pylint: disable=too-many-locals
# So sorry :-p
def solve(data, move, faces=None, is_sample=False):
    board: list[list[Tile]] = []
    width = 0
    for line in data:
        if line == "":
            break
        board.append([Tile(char) for char in line])
        width = max(width, len(line))

    for line in board:
        if len(line) < width:
            to_add = width - len(line)
            line.extend([Tile.NO_TILE] * to_add)

    instructions = data[-1]

    current_pos = Position(x=board[0].index(Tile.OPEN), y=0)
    current_fac = Tile.EAST

    for instruction in re.findall(r"([RL]?\d+)", instructions):
        # turn
        if instruction.startswith("L"):
            current_fac = DIRECTIONS[
                (DIRECTIONS.index(current_fac) - 1) % len(DIRECTIONS)
            ]
            instruction = instruction[1:]
        elif instruction.startswith("R"):
            current_fac = DIRECTIONS[
                (DIRECTIONS.index(current_fac) + 1) % len(DIRECTIONS)
            ]
            instruction = instruction[1:]

        # move
        direction = deepcopy(current_fac)
        new_pos, current_fac = move(
            current_pos, current_fac, board, faces, is_sample
        )
        for _ in range(int(instruction)):
            if board[new_pos.y][new_pos.x] == Tile.SOLID:
                # solid, so stop this instruction
                board[current_pos.y][current_pos.x] = direction
                new_pos = current_pos
                break

            board[current_pos.y][current_pos.x] = direction
            current_pos = new_pos
            direction = deepcopy(current_fac)
            new_pos, current_fac = move(
                current_pos, current_fac, board, faces, is_sample
            )

    row = current_pos.y + 1
    col = current_pos.x + 1
    fac = DIRECTIONS.index(direction)

    print(row, col, fac)
    return 1000 * row + 4 * col + fac


def p1(data, is_sample):
    return solve(data, move_p1)


def p2(data, is_sample):
    # faces are numbered like a regular 6-sided die
    if is_sample:
        sidelen = 4
        face_1 = Face(
            2 * sidelen,
            3 * sidelen - 1,
            1 * sidelen,
            2 * sidelen - 1,
        )
        face_2 = Face(
            2 * sidelen,
            3 * sidelen - 1,
            2 * sidelen,
            3 * sidelen - 1,
        )
        face_3 = Face(
            3 * sidelen,
            4 * sidelen - 1,
            2 * sidelen,
            3 * sidelen - 1,
        )
        face_4 = Face(
            1 * sidelen,
            2 * sidelen - 1,
            1 * sidelen,
            2 * sidelen - 1,
        )
        face_5 = Face(
            2 * sidelen,
            3 * sidelen - 1,
            0 * sidelen,
            1 * sidelen - 1,
        )
        face_6 = Face(
            0 * sidelen,
            1 * sidelen - 1,
            1 * sidelen,
            2 * sidelen - 1,
        )
    else:
        sidelen = 50
        face_1 = Face(
            1 * sidelen,
            2 * sidelen - 1,
            0 * sidelen,
            1 * sidelen - 1,
        )
        face_2 = Face(
            1 * sidelen,
            2 * sidelen - 1,
            1 * sidelen,
            2 * sidelen - 1,
        )
        face_3 = Face(
            2 * sidelen,
            3 * sidelen - 1,
            0 * sidelen,
            1 * sidelen - 1,
        )
        face_4 = Face(
            0 * sidelen,
            1 * sidelen - 1,
            2 * sidelen,
            3 * sidelen - 1,
        )
        face_5 = Face(
            0 * sidelen,
            1 * sidelen - 1,
            3 * sidelen,
            4 * sidelen - 1,
        )
        face_6 = Face(
            1 * sidelen,
            2 * sidelen - 1,
            2 * sidelen,
            3 * sidelen - 1,
        )

    faces = (face_1, face_2, face_3, face_4, face_5, face_6)

    return solve(data, move_p2, faces, is_sample)
