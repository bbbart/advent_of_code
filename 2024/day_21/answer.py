#!/usr/bin/env python

from collections import deque
from itertools import pairwise

NUMERIC_KEYPAD = {
    "A": [("3", "^"), ("0", "<")],
    "0": [("2", "^"), ("A", ">")],
    "1": [("4", "^"), ("2", ">")],
    "2": [("5", "^"), ("3", ">"), ("0", "v"), ("1", "<")],
    "3": [("6", "^"), ("A", "v"), ("2", "<")],
    "4": [("7", "^"), ("5", ">"), ("1", "v")],
    "5": [("8", "^"), ("6", ">"), ("2", "v"), ("4", "<")],
    "6": [("9", "^"), ("3", "v"), ("5", "<")],
    "7": [("8", ">"), ("4", "v")],
    "8": [("9", ">"), ("5", "v"), ("7", "<")],
    "9": [("6", "v"), ("8", "<")],
}

DIRECTIONAL_KEYPAD = {
    "A": [(">", "v"), ("^", "<")],
    "^": [("A", ">"), ("v", "v")],
    "<": [("v", ">")],
    "v": [("^", "^"), (">", ">"), ("<", "<")],
    ">": [("A", "^"), ("v", "<")],
}

BFS_CACHE = {}


def is_valid_path(path, graph, source):
    if not path:
        return True
    try:
        nkey = [k for (k, s) in graph[source] if s == path[0]][0]
    except IndexError:
        return False

    return is_valid_path(path[1:], graph, nkey)


def optimized_path(path, graph, source):
    distinct_steps = set(path)
    if len(distinct_steps) < 2:
        return path

    opath = "".join(sorted(path, key="<v>^".index))
    if is_valid_path(opath, graph, source):
        return opath

    return path


def bfs(source, sink, graph):
    if (source, sink) in BFS_CACHE:
        return BFS_CACHE[(source, sink)]

    queue = deque()
    explored = set()

    queue.append((source, ""))
    explored.add(source)

    while queue:
        key, path = queue.popleft()
        if key == sink:
            opath = optimized_path(path, graph, source) + "A"
            BFS_CACHE[(source, sink)] = opath
            return opath
        for nkey, npath in graph[key]:
            if nkey not in explored:
                queue.append((nkey, path + npath))
                explored.add(nkey)

    return None


# pylint: disable=too-many-locals
def p1(data: list[str], is_sample: bool):
    codes = data

    procedures = {}
    for code in codes:
        procedure = ""
        for source, sink in pairwise("A" + code):
            procedure += bfs(source, sink, NUMERIC_KEYPAD)
        procedures[code] = procedure

    procedures2 = {}
    codes = set()
    for code, procedure in procedures.items():
        procedure2 = ""
        for source, sink in pairwise("A" + procedure):
            procedure2 += bfs(source, sink, DIRECTIONAL_KEYPAD)
        procedures2[code] = procedure2

    procedures3 = {}
    codes = set()
    for code, procedure in procedures2.items():
        procedure3 = ""
        for source, sink in pairwise("A" + procedure):
            procedure3 += bfs(source, sink, DIRECTIONAL_KEYPAD)
        procedures3[code] = procedure3

    total = 0
    for code, procedure in procedures3.items():
        numval = int("".join(char for char in code if char != "A"))
        seqlen = len(procedure)
        total += numval * seqlen

    return total


def p2(data: list[str], is_sample: bool):
    # I am convinced this returns the correct answer, but the process gets
    # killed after step 20/25. :-(
    #
    # Perhaps some more intelligence is required to shortcut some heavy
    # calculations. I am guessing that one can start looking at recurring
    # patterns and predict what they will look like after X keypads.
    if is_sample:
        return "N/A"

    codes = data

    procedures = {}
    for code in codes:
        procedure = ""
        for source, sink in pairwise("A" + code):
            procedure += bfs(source, sink, NUMERIC_KEYPAD)
        procedures[code] = procedure

    for _ in range(25):
        for code, procedure in procedures.items():
            new_procedure = ""
            for source, sink in pairwise("A" + procedure):
                new_procedure += bfs(source, sink, DIRECTIONAL_KEYPAD)
            procedures[code] = new_procedure

    total = 0
    for code, procedure in procedures.items():
        numval = int("".join(char for char in code if char != "A"))
        seqlen = len(procedure)
        total += numval * seqlen

    return total
