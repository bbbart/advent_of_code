import warnings
from collections import defaultdict


def parse_input(data):
    tempstacks = defaultdict(list)

    while True:
        line = data.pop(0)
        if line == "":
            break
        for index in range(1, len(line), 4):
            char = line[index]
            if char != " ":
                tempstacks[index] += char

    stacks = defaultdict(list)
    for _, stack in tempstacks.items():
        realname = stack.pop()
        stacks[realname] = list(reversed(stack))

    return stacks


def p1(data):
    stacks_p1 = parse_input(data)
    for line in data:
        if not line.startswith("move"):
            warnings.warn(f"not a move instruction: {line}")

        instruction_parts = line.split()
        amount = int(instruction_parts[1])
        stack_from = instruction_parts[3]
        stack_to = instruction_parts[5]
        for _ in range(amount):
            stacks_p1[stack_to].append(stacks_p1[stack_from].pop())

    result = ""
    for stackname in sorted(stacks_p1.keys()):
        result += stacks_p1[stackname][-1]

    return result


def p2(data):
    stacks_p2 = parse_input(data)

    for line in data:
        if not line.startswith("move"):
            warnings.warn(f"not a move instruction: {line}")

        instruction_parts = line.split()
        amount = int(instruction_parts[1])
        stack_from = instruction_parts[3]
        stack_to = instruction_parts[5]
        stacks_p2[stack_to].extend(stacks_p2[stack_from][-amount:])
        del stacks_p2[stack_from][-amount:]

    result = ""
    for stackname in sorted(stacks_p2.keys()):
        result += stacks_p2[stackname][-1]

    return result
