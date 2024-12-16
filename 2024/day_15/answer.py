#!/usr/bin/env python


def visualise(warehouse, robot):
    width = max(p[0] for p in warehouse) + 1
    height = max(p[1] for p in warehouse) + 1
    for y in range(height):
        print("")
        for x in range(width):
            if (x, y) == robot:
                print("@", end="")
            else:
                print(warehouse.get((x, y), "."), end="")


# pylint: disable=too-many-locals,too-many-branches
def p1(data: list[str], is_sample: bool):
    warehouse: dict[tuple[int], chr] = {}
    moves: list[chr] = []
    robot: tuple[int] = None

    parttwo = False
    for y, line in enumerate(data):
        if not line:
            parttwo = True
            continue
        for x, char in enumerate(line):
            if not parttwo:
                if char == "@":
                    robot = (x, y)
                    continue
                if char != ".":
                    warehouse[(x, y)] = char
            else:
                moves.append(char)

    steps = {"<": (-1, 0), ">": (1, 0), "v": (0, 1), "^": (0, -1)}

    for move in moves:
        new_pos = (robot[0] + steps[move][0], robot[1] + steps[move][1])
        if new_pos not in warehouse:
            robot = new_pos
            continue
        if warehouse[new_pos] == "#":
            continue
        # now the only option is that we are attempting to push boxes
        boxes_to_push: list[tuple[int]] = []
        boxes_to_push.append(new_pos)
        next_pos = new_pos
        while True:
            next_pos = (
                next_pos[0] + steps[move][0],
                next_pos[1] + steps[move][1],
            )
            if next_pos not in warehouse:
                for pos in reversed(boxes_to_push):
                    del warehouse[pos]
                    warehouse[
                        (pos[0] + steps[move][0], pos[1] + steps[move][1])
                    ] = "O"
                robot = new_pos
                break
            if warehouse[next_pos] == "O":
                boxes_to_push.append(next_pos)
                continue
            # we hit a wall
            break

    return sum(
        pos[0] + 100 * pos[1] for pos, char in warehouse.items() if char == "O"
    )


# pylint: disable=too-many-statements
def p2(data: list[str], is_sample: bool):
    warehouse: dict[tuple[int], chr] = {}
    moves: list[chr] = []
    robot: tuple[int] = None

    parttwo = False
    for y, line in enumerate(data):
        if not line:
            parttwo = True
            continue
        x = 0
        for char in line:
            if not parttwo:
                if char == "@":
                    robot = (x, y)
                elif char == "#":
                    warehouse[(x, y)] = char
                    warehouse[(x + 1, y)] = char
                elif char == "O":
                    warehouse[(x, y)] = "["
                    warehouse[(x + 1, y)] = "]"
                x += 2
            else:
                moves.append(char)

    steps = {"<": (-1, 0), ">": (1, 0), "v": (0, 1), "^": (0, -1)}
    for move in moves:
        new_pos = (robot[0] + steps[move][0], robot[1] + steps[move][1])
        if new_pos not in warehouse:
            robot = new_pos
            continue
        if warehouse[new_pos] == "#":
            continue
        # now the only option is that we are attempting to push boxes
        boxes_to_push: set[tuple[int]] = set()
        cells_to_check: set[tuple[int]] = set()
        cells_checked: set[tuple[int]] = set()

        cells_to_check.add(new_pos)
        boxes_to_push.add(new_pos)
        if warehouse[new_pos] == "[":
            cells_to_check.add((new_pos[0] + 1, new_pos[1]))
            boxes_to_push.add((new_pos[0] + 1, new_pos[1]))
        else:
            cells_to_check.add((new_pos[0] - 1, new_pos[1]))
            boxes_to_push.add((new_pos[0] - 1, new_pos[1]))
        done = False
        while not done:
            while cells_to_check - cells_checked:
                cell = (cells_to_check - cells_checked).pop()
                cells_checked.add(cell)
                next_pos = (
                    cell[0] + steps[move][0],
                    cell[1] + steps[move][1],
                )
                if next_pos not in warehouse:
                    continue
                if warehouse[next_pos] == "[":
                    boxes_to_push.add(next_pos)
                    boxes_to_push.add((next_pos[0] + 1, next_pos[1]))
                    cells_to_check.add(next_pos)
                    cells_to_check.add((next_pos[0] + 1, next_pos[1]))
                    continue
                if warehouse[next_pos] == "]":
                    boxes_to_push.add(next_pos)
                    boxes_to_push.add((next_pos[0] - 1, next_pos[1]))
                    cells_to_check.add(next_pos)
                    cells_to_check.add((next_pos[0] - 1, next_pos[1]))
                    continue
                if warehouse[next_pos] == "#":
                    # we hit a wall
                    done = True
                    break
            else:
                for box in boxes_to_push:
                    match move:
                        # pylint: disable=unnecessary-lambda-assignment
                        case "<":
                            sort_key = lambda p: p[0]
                        case ">":
                            sort_key = lambda p: -p[0]
                        case "^":
                            sort_key = lambda p: p[1]
                        case "v":
                            sort_key = lambda p: -p[1]

                    for box in sorted(boxes_to_push, key=sort_key):
                        warehouse[
                            (
                                box[0] + steps[move][0],
                                box[1] + steps[move][1],
                            )
                        ] = warehouse[box]
                        del warehouse[box]
                    robot = new_pos
                    done = True
                    break
    return sum(
        pos[0] + 100 * pos[1] for pos, char in warehouse.items() if char == "["
    )
