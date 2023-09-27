import curses
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


def p1(data, is_sample):
    source = map(int, data[0].split(","))
    arcade = intcode(source, lambda: 0)

    block_counter = 0
    while True:
        try:
            _, _, tile_id = next(arcade), next(arcade), next(arcade)
            if tile_id == 2:
                block_counter += 1
        except StopIteration:
            return block_counter


def p2(data, is_sample):
    source = list(map(int, data[0].split(",")))
    source[0] = 2

    def inputfunc(positions):
        def getinput():
            if positions["ball"] < positions["pad"]:
                return -1
            if positions["ball"] > positions["pad"]:
                return 1
            return 0

        return getinput

    x_positions: dict[str, int] = {"ball": -1, "pad": -1}
    arcade = intcode(source, inputfunc(x_positions))

    # let's play
    score = -1
    while True:
        try:
            x, y, tile_id = next(arcade), next(arcade), next(arcade)
        except StopIteration:
            return score

        if (x, y) == (-1, 0):
            score = tile_id
            continue

        if tile_id == 4:
            x_positions["ball"] = x
        elif tile_id == 3:
            x_positions["pad"] = x


def p2_curses(data, is_sample):
    source = list(map(int, data[0].split(",")))
    source[0] = 2

    def game(stdscr):
        stdscr.clear()

        x_positions: dict[str, int] = {"ball": -1, "pad": -1}

        def inputfunc(positions):
            def getinput():
                if positions["ball"] < positions["pad"]:
                    return -1
                if positions["ball"] > positions["pad"]:
                    return 1
                return 0

            return getinput

        arcade = intcode(source, inputfunc(x_positions))
        tiles = [" ", "#", "=", "_", "o"]

        # initial drawing
        max_y = 0
        while True:
            x, y, tile_id = next(arcade), next(arcade), next(arcade)
            max_y = max(max_y, y)
            if (x, y) == (-1, 0):
                score = tile_id
                break

            if tile_id == 4:  # ball
                x_positions["ball"] = x
            elif tile_id == 3:  # pad
                x_positions["pad"] = x
            stdscr.addch(y, x, tiles[tile_id])

        # let's play
        while True:
            try:
                x, y, tile_id = next(arcade), next(arcade), next(arcade)
            except StopIteration:
                return score

            if (x, y) == (-1, 0):
                score = tile_id
                continue

            if tile_id == 4:  # ball
                x_positions["ball"] = x
            elif tile_id == 3:  # pad
                x_positions["pad"] = x

            stdscr.addch(y, x, tiles[tile_id])
            stdscr.addstr(
                max_y + 1,
                0,
                f"score: {score}, ball_x: {x_positions['ball']}, pad_x: {x_positions['pad']}",
            )
            stdscr.refresh()

            time.sleep(0.001)

    return curses.wrapper(game)
