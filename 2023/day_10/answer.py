#!/usr/bin/env python

box_char = {
    "|": "│",
    "-": "─",
    "L": "└",
    "J": "┘",
    "7": "┐",
    "F": "┌",
    ".": " ",
}


def map_pipes(
    data,
) -> tuple[dict[tuple[int, int], list[tuple[int, int]]], tuple[int, int]]:
    graph: dict[tuple[int, int], list[tuple[int, int]]] = {}
    start_pos = None
    for y, line in enumerate(data):
        for x, row in enumerate(line):
            match row:
                case "|":
                    graph[(x, y)] = [(x, y - 1), (x, y + 1)]
                case "-":
                    graph[(x, y)] = [(x - 1, y), (x + 1, y)]
                case "L":
                    graph[(x, y)] = [(x + 1, y), (x, y - 1)]
                case "J":
                    graph[(x, y)] = [(x, y - 1), (x - 1, y)]
                case "7":
                    graph[(x, y)] = [(x - 1, y), (x, y + 1)]
                case "F":
                    graph[(x, y)] = [(x, y + 1), (x + 1, y)]
                case ".":
                    graph[(x, y)] = []
                case "S":
                    graph[(x, y)] = []
                    start_pos = (x, y)

    # figure out the shape of the pipe at the starting position
    for pos, conn in graph.items():
        if start_pos in conn:
            graph[start_pos].append(pos)

    assert len(graph[start_pos]) == 2

    return graph, start_pos


def p1(data, is_sample):
    pipes, start_pos = map_pipes(data)

    # crawl the pipe in two opposite directions and see where we cross
    crawl1, crawl2 = pipes[start_pos]
    visited = set()
    visited.add(start_pos)
    while crawl1 != crawl2:
        visited |= {crawl1, crawl2}
        try:
            crawl1 = (set(pipes[crawl1]) - visited).pop()
            crawl2 = (set(pipes[crawl2]) - visited).pop()
        except KeyError:
            break

    return (len(visited) + 1) // 2


def p2(data, is_sample):
    pipes, start_pos = map_pipes(data)

    # find our looping pipe structure
    loop = set()
    crawler = start_pos
    while True:
        loop.add(crawler)
        try:
            crawler = (set(pipes[crawler]) - loop).pop()
        except KeyError:
            break

    # determine the pipe of the starting position
    if set(pipes[start_pos]) == {
        (start_pos[0], start_pos[1] - 1),
        (start_pos[0], start_pos[1] + 1),
    }:
        start_char = "|"
    elif set(pipes[start_pos]) == {
        (start_pos[0], start_pos[1] - 1),
        (start_pos[0] - 1, start_pos[1]),
        (start_pos[0] + 1, start_pos[1]),
    }:
        start_char = "-"
    elif set(pipes[start_pos]) == {
        (start_pos[0], start_pos[1] - 1),
        (start_pos[0] + 1, start_pos[1]),
    }:
        start_char = "L"
    elif set(pipes[start_pos]) == {
        (start_pos[0], start_pos[1] - 1),
        (start_pos[0] - 1, start_pos[1]),
    }:
        start_char = "J"
    elif set(pipes[start_pos]) == {
        (start_pos[0] - 1, start_pos[1]),
        (start_pos[0], start_pos[1] + 1),
    }:
        start_char = "7"
    elif set(pipes[start_pos]) == {
        (start_pos[0] + 1, start_pos[1]),
        (start_pos[0], start_pos[1] + 1),
    }:
        start_char = "F"

    # starting figuring our how many tiles are inside
    # implements a simple line sweep algorithm
    in_counter = 0
    for y, line in enumerate(data):
        inout = False
        horizontal_wall = ""
        for x, char in enumerate(line):
            if char == "S":
                char = start_char

            # if we encounter a tile not part of the loop, our state doesn't
            # change, but our counter (potentially) does
            if (x, y) not in loop:
                in_counter += 1 if inout else 0
                # print("I" if inout else ".", end="")
                continue

            # if we encounter a tile part of the loop, our state changes, but
            # our counter doesn't
            if char == "|":
                inout = not inout
            else:
                horizontal_wall += char

            if char in ("7", "J"):
                if (
                    horizontal_wall.startswith("F")
                    and horizontal_wall.endswith("J")
                ) or (
                    horizontal_wall.startswith("L")
                    and horizontal_wall.endswith("7")
                ):
                    # 'winding' horizontal_wall, not 'looping' horizontal_wall
                    inout = not inout
                horizontal_wall = ""

            # print(box_char[char], end="")

    return in_counter
