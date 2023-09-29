import curses
import sys
import time
from collections import defaultdict
from typing import Callable


# pylint: disable=too-many-branches,too-many-statements,too-many-locals
def intcode(instructions, inputfunc: Callable):
    memory = defaultdict(int)
    for address, value in enumerate(instructions):
        memory[address] = value

    # describes how the parameters work for the different opcodes:
    #   0: read parameter
    #   1: write paremter (can never be in immesdiate mode)
    param_types: dict[int, int] = {
        1: (0, 0, 1),  # ADD
        2: (0, 0, 1),  # MULTIPLY
        3: (1,),  # INPUT
        4: (0,),  # OUTPUT
        5: (0, 0),  # JUMP-IF-TRUE
        6: (0, 0),  # JUMP-IF-FALSE
        7: (0, 0, 1),  # LESS THAN
        8: (0, 0, 1),  # EQUALS
        9: (0,),  # ADJUST RELATIVE BASE
        99: (),  # EXIT
    }

    pointer = 0
    relbase = 0
    while True:
        instruction = str(memory[pointer]).zfill(5)

        # 0: position mode
        # 1: immediate mode
        # 2: relative mode
        param_modes = tuple(map(int, instruction[:-2][::-1]))
        opcode = int(instruction[-2:])

        params = []
        for index, (param_type, mode) in enumerate(
            zip(param_types[opcode], param_modes), start=1
        ):
            if param_type == 0:  # read parameter
                if mode == 2:
                    param = memory[relbase + memory[pointer + index]]
                elif mode == 1:
                    param = memory[pointer + index]
                elif mode == 0:
                    param = memory[memory[pointer + index]]
                else:
                    raise ValueError(f"Unknown mode for read parameter: {mode}")
            elif param_type == 1:  # write parameter
                if mode == 2:
                    param = relbase + memory[pointer + index]
                elif mode == 0:
                    param = memory[pointer + index]
                else:
                    raise ValueError(
                        f"Unknown mode for write parameter: {mode}"
                    )
            else:
                raise ValueError(f"Unknown parameters type: {param_type}")

            params.append(param)

        if opcode == 1:  # ADD
            memory[params[2]] = params[0] + params[1]

            pointer += len(params) + 1
        elif opcode == 2:  # MULTIPLY
            memory[params[2]] = params[0] * params[1]

            pointer += len(params) + 1
        elif opcode == 3:  # INPUT
            value = inputfunc()
            memory[params[0]] = value

            pointer += len(params) + 1
        elif opcode == 4:  # OUTPUT
            yield params[0]

            pointer += len(params) + 1
        elif opcode == 5:  # JUMP-IF-TRUE
            if params[0]:
                pointer = params[1]
            else:
                pointer += len(params) + 1
        elif opcode == 6:  # JUMP-IF-FALSE
            if not params[0]:
                pointer = params[1]
            else:
                pointer += len(params) + 1
        elif opcode == 7:  # LESS THAN
            if params[0] < params[1]:
                memory[params[2]] = 1
            else:
                memory[params[2]] = 0

            pointer += len(params) + 1
        elif opcode == 8:  # EQUALS
            if params[0] == params[1]:
                memory[params[2]] = 1
            else:
                memory[params[2]] = 0

            pointer += len(params) + 1
        elif opcode == 9:  # ADJUST RELATIVE BASE
            relbase += params[0]

            pointer += len(params) + 1
        elif opcode == 99:
            return
        else:
            raise ValueError(f"ERROR: unknown opcode {opcode}")


def p1_curses(data, is_sample):
    source = list(map(int, data[0].split(",")))

    def game(stdscr):
        stdscr.clear()
        stdscr.nodelay(False)
        curses.noecho()

        # pylint: disable=inconsistent-return-statements
        def inputfunc(direction: list[int]):
            def move():
                keydirs = {
                    curses.KEY_UP: 1,
                    curses.KEY_DOWN: 2,
                    curses.KEY_LEFT: 3,
                    curses.KEY_RIGHT: 4,
                }
                while key := stdscr.getch():
                    if key == ord("q"):
                        sys.exit(1)
                    if key not in keydirs:
                        continue
                    direction[0] = keydirs[key]
                    return keydirs[key]

            return move

        direction = [None]
        robot = intcode(source, inputfunc(direction))
        tiles = ["#", ".", "O", "D"]

        # initial drawing
        pos = (0, 0)
        stdscr.addch(pos[1] + 20, pos[0] + 20, tiles[-1])

        # let's play
        moves = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
        while True:
            tile_id = next(robot)
            new_pos = tuple(map(sum, zip(pos, moves[direction[0]])))
            match tile_id:
                case 0:
                    stdscr.addch(
                        new_pos[1] + 20, new_pos[0] + 20, tiles[tile_id]
                    )
                case 1:
                    stdscr.addch(pos[1] + 20, pos[0] + 20, tiles[tile_id])
                    pos = new_pos
                case 2:
                    return new_pos

            stdscr.addch(pos[1] + 20, pos[0] + 20, tiles[-1])
            stdscr.addstr(0, 0, str(pos))
            stdscr.refresh()

    return curses.wrapper(game)


def p1(data, is_sample):
    source = list(map(int, data[0].split(",")))

    def mover(direction):
        def move():
            return direction[0]

        return move

    next_move = [1]
    robot = intcode(source, mover(next_move))

    stack = []
    visited = set()
    parent = {}

    start = (0, 0)
    stack.append(start)
    parent[start] = None

    def move_robot(direction: int) -> int:
        next_move[0] = direction
        return next(robot)

    moves = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}

    while stack:
        x, y = stack[-1]
        visited.add((x, y))

        for direction, (dx, dy) in moves.items():
            new_x, new_y = x + dx, y + dy

            if (new_x, new_y) in visited:
                continue

            tile = move_robot(direction)

            if tile == 0:
                continue

            parent[(new_x, new_y)] = (x, y)

            if tile == 1:
                stack.append((new_x, new_y))
                break

            if tile == 2:
                path = [(new_x, new_y)]
                while parent[path[-1]] is not None:
                    path.append(parent[path[-1]])
                return len(path) - 1
        else:
            stack.pop()
            if stack:
                backtrack_x, backtrack_y = stack[-1]
                for direction, (dx, dy) in moves.items():
                    if backtrack_x == x + dx and backtrack_y == y + dy:
                        move_robot(direction)
                        break


def p2_curses(data, is_sample):
    source = list(map(int, data[0].split(",")))

    def mover(direction):
        def move():
            return direction[0]

        return move

    next_move = [1]
    robot = intcode(source, mover(next_move))

    maze = {}
    x, y = 0, 0

    stack = [(x, y, iter([1, 2, 3, 4]))]

    def move_robot(direction: int) -> int:
        next_move[0] = direction
        return next(robot)

    def draw(stdscr):
        directions = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
        oxygen_source = (None, None)

        while stack:
            x, y, dir_iter = stack[-1]
            if (x, y) not in maze:
                maze[(x, y)] = []

            for d in dir_iter:
                dx, dy = directions[d]
                new_x, new_y = x + dx, y + dy

                if (new_x, new_y) in maze:
                    continue

                result = move_robot(d)

                if result == 0:
                    maze[(new_x, new_y)] = []
                    stdscr.addch(new_y + 40, new_x + 40, "#")
                if result == 2:
                    oxygen_source = (new_x, new_y)
                    stdscr.addch(new_y + 40, new_x + 40, "O", curses.A_REVERSE)
                if result in (1, 2):
                    maze[(x, y)].append((new_x, new_y))
                    maze[(new_x, new_y)] = [(x, y)]
                    stack.append((new_x, new_y, iter([1, 2, 3, 4])))
                    stdscr.addch(new_y + 40, new_x + 40, ".")
                    if (new_x, new_y) == oxygen_source:
                        stdscr.addch(
                            new_y + 40, new_x + 40, "O", curses.A_REVERSE
                        )
                    break
            else:
                stack.pop()
                if stack:
                    prev_x, prev_y, _ = stack[-1]
                    for d, (dx, dy) in directions.items():
                        if prev_x == x + dx and prev_y == y + dy:
                            move_robot(d)
                            break

        tofill = set(space for space, neigbours in maze.items() if neigbours)
        filled = {oxygen_source}

        timer = 0
        while tofill != filled:
            for x, y in filled:
                stdscr.addch(y + 40, x + 40, "O", curses.A_REVERSE)
            stdscr.getch()
            fill = set()
            for space in filled:
                fill |= set(maze[space])
            filled |= fill
            timer += 1

        return timer

    return curses.wrapper(draw)


def p2(data, is_sample):
    source = list(map(int, data[0].split(",")))

    def mover(direction):
        def move():
            return direction[0]

        return move

    next_move = [1]
    robot = intcode(source, mover(next_move))

    maze = {}
    x, y = 0, 0

    stack = [(x, y)]

    def move_robot(direction: int) -> int:
        next_move[0] = direction
        return next(robot)

    directions = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
    oxygen_source = (None, None)

    while stack:
        x, y = stack[-1]
        if (x, y) not in maze:
            maze[(x, y)] = []

        for d, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy

            if (new_x, new_y) in maze:
                continue

            result = move_robot(d)

            if result == 0:
                maze[(new_x, new_y)] = []
            if result == 2:
                oxygen_source = (new_x, new_y)
            if result in (1, 2):
                maze[(x, y)].append((new_x, new_y))
                maze[(new_x, new_y)] = [(x, y)]
                stack.append((new_x, new_y))
                break
        else:
            stack.pop()
            if stack:
                prev_x, prev_y = stack[-1]
                for d, (dx, dy) in directions.items():
                    if prev_x == x + dx and prev_y == y + dy:
                        move_robot(d)
                        break

    tofill = set(space for space, neigbours in maze.items() if neigbours)
    filled = {oxygen_source}

    timer = 0
    while tofill != filled:
        fill = set()
        for space in filled:
            fill |= set(maze[space])
        filled |= fill
        timer += 1

    return timer
