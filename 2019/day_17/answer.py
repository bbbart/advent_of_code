from collections import defaultdict
from itertools import chain, cycle
from queue import SimpleQueue
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

        # PARAM MODES:
        # 0: position mode
        # 1: immediate mode
        # 2: relative mode
        param_modes = map(int, instruction[:-2][::-1])
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
    source = list(map(int, data[0].split(",")))

    robot = intcode(source, lambda: 0)

    scaffolds = set()

    x, y = 0, 0
    for i in robot:
        if chr(i) == "#":
            scaffolds.add((x, y))
        elif i == 10:
            x = -1
            y += 1
        x += 1

    intersections = set()
    for co_x, co_y in scaffolds:
        neighbours = set(
            (
                (co_x - 1, co_y),
                (co_x + 1, co_y),
                (co_x, co_y - 1),
                (co_x, co_y + 1),
            )
        )
        if neighbours.issubset(scaffolds):
            intersections.add((co_x, co_y))

    return sum(x * y for x, y in intersections)


def p2(data, is_sample):
    source = list(map(int, data[0].split(",")))
    robot = intcode(source, lambda: 0)

    # scan the area
    scaffolds = set()
    vacuum_orientation = None
    vacuum_position = None, None
    x, y = 0, 0
    for i in robot:
        match chr(i):
            case "^" | ">" | "v" | "<":
                vacuum_position = x, y
                vacuum_orientation = chr(i)
            case "#":
                scaffolds.add((x, y))
            case "\n":
                x = -1
                y += 1
        x += 1

    intersections = set()
    for co_x, co_y in scaffolds:
        neighbours = set(
            (
                (co_x - 1, co_y),
                (co_x + 1, co_y),
                (co_x, co_y - 1),
                (co_x, co_y + 1),
            )
        )
        if neighbours.issubset(scaffolds):
            intersections.add((co_x, co_y))

    # map the scaffolds in a set of staight lines
    cur_pos = vacuum_position
    directions = {"R": (1, 0), "L": (-1, 0), "D": (0, 1), "U": (0, -1)}
    path = [cur_pos]
    walkway = ""
    dirs_looked_at = 0
    for direction, deltas in cycle(directions.items()):
        while True:
            peek_pos = tuple(map(sum, zip(cur_pos, deltas)))
            if peek_pos in path and peek_pos not in intersections:
                break
            if peek_pos in scaffolds:
                path.append(peek_pos)
                walkway += direction
                cur_pos = peek_pos
                dirs_looked_at = 1
            else:
                dirs_looked_at += 1
                break
        if dirs_looked_at >= 4:
            break

    # convert these straight lines into a set of vacuum instructions
    instructions = []
    going_to = walkway[0]
    match vacuum_orientation, going_to:
        case ("^", "R") | ("<", "U") | ("v", "L") | (">", "D"):
            instructions.extend(["R", 1])
        case ("^", "L") | ("<", "D") | ("v", "R") | (">", "U"):
            instructions.extend(["L", 1])
        case ("^", "U") | ("<", "L") | ("v", "D") | (">", "R"):
            instructions.extend([1])
        case ("^", "D") | ("<", "R") | ("v", "U") | (">", "L"):
            instructions.extend(["R", "R", 1])

    for w in walkway[1:]:
        match going_to, w:
            case ("R", "D") | ("U", "R") | ("L", "U") | ("D", "L"):
                instructions.extend(["R", 1])
            case ("R", "U") | ("U", "L") | ("L", "D") | ("D", "R"):
                instructions.extend(["L", 1])
            case ("R", "R") | ("U", "U") | ("L", "L") | ("D", "D"):
                instructions[-1] += 1
            case _:
                raise ValueError("Cannot backtrace...")

        going_to = w

    # search for pattern partitions in the instructions
    all_instructions = [
        (instructions[i], instructions[i + 1])
        for i in range(0, len(instructions), 2)
    ]

    def replace_pattern_with(full_list, pattern, replacement):
        new_list = []
        i = 0
        while i < len(full_list):
            if full_list[i : i + len(pattern)] == pattern:
                new_list.append(replacement)
                i += len(pattern)
            else:
                new_list.append(full_list[i])
                i += 1

        return new_list

    def find_pattern(full_list, pattern_length):
        pattern = []
        i = 0
        while i < len(full_list):
            el = full_list[i]
            if isinstance(el, tuple):
                pattern.append(el)
                if len(pattern) == pattern_length:
                    return pattern
            else:
                pattern = []
            i += 1
        return None

    def find_partitions(
        instructions,
        max_pattern_len,
        max_pattern_count,
        pattern_dict,
        pattern_count=0,
    ):
        partitions = []

        if all(isinstance(el, str) for el in instructions):
            partitions.append({**pattern_dict, "routine": instructions})
            return partitions

        if pattern_count >= max_pattern_count:
            return []

        next_pattern_name = chr(65 + pattern_count)  # 'A', 'B', 'C', ...

        for pattern_len in range(1, max_pattern_len + 1):
            pattern = find_pattern(instructions, pattern_len)
            if not pattern:
                continue
            remainder = replace_pattern_with(
                instructions, pattern, next_pattern_name
            )

            new_pattern_dict = {
                **pattern_dict,
                f"func_{next_pattern_name}": pattern,
            }

            sub_partitions = find_partitions(
                remainder,
                max_pattern_len,
                max_pattern_count,
                new_pattern_dict,
                pattern_count + 1,
            )
            partitions.extend(sub_partitions)

        return partitions

    max_pattern_len = 10
    max_pattern_count = 3
    partitions = find_partitions(
        all_instructions, max_pattern_len, max_pattern_count, {}
    )

    if not partitions:
        return "No partitions found...?"

    # select for the most memory efficient one :-)
    smallest_partition = min(
        partitions, key=lambda p: sum(map(len, p.values()))
    )

    # and run it
    source = list(map(int, data[0].split(",")))
    source[0] = 2

    def mover(partition):
        moves = SimpleQueue()
        for func in ("routine", "func_A", "func_B", "func_C"):
            instruction_set = partition[func]
            for instr in map(str, ",".join(map(str, chain(*instruction_set)))):
                moves.put_nowait(ord(instr))
            moves.put_nowait(ord("\n"))

        moves.put_nowait(ord("n"))
        moves.put_nowait(ord("\n"))

        def next_move():
            return moves.get_nowait()

        return next_move

    robot = intcode(source, mover(smallest_partition))

    retval = None
    for retval in robot:
        pass

    return retval
