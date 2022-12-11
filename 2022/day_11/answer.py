from dataclasses import dataclass
from functools import reduce
from inspect import stack
from math import floor

from sympy import sympify


@dataclass
class Item:
    worry_level: int


class Monkey:
    def __init__(self, monkey_def):
        self.inspection_count = 0
        self.branches = {}
        for line in monkey_def:
            line = line.strip().lower()
            if line.startswith("monkey"):
                self.id_ = int(line.split()[1][0])
            elif line.startswith("starting items"):
                self.items = list(
                    map(Item, map(int, line.split(":")[1].split(",")))
                )
            elif line.startswith("operation"):
                full_operation = line.split(":")[1]
                self.new = sympify(full_operation.split("=")[1])
            elif line.startswith("test"):
                self.div_test = int(line.split()[-1])
            elif line.startswith("if"):
                conditional = line.split()[1][:-1] == "true"
                target = int(line.split()[-1])
                self.branches[conditional] = target

    def take_turn(self, mod=0):
        while self.items:
            item = self.items.pop(0)
            item.worry_level = self.new.subs({"old": item.worry_level})
            self.inspection_count += 1

            caller_name = stack()[1][3]
            if caller_name == "p1":
                item.worry_level = floor(item.worry_level / 3)

            if mod:
                item.worry_level %= mod

            yield (item, self.branches[item.worry_level % self.div_test == 0])

    def __repr__(self):
        return (
            f"<Monkey {self.id_} has items {self.items} and tests for "
            f"divisibility by {self.div_test} after operation {self.new}; "
            f"it decides as follows: {self.branches}>"
        )


def create_monkeys(data):
    monkey_def = []
    monkeys = []
    for line in data:
        if line == "":
            monkeys.append(Monkey(monkey_def))
            monkey_def = []
            continue
        monkey_def.append(line)
    monkeys.append(Monkey(monkey_def))

    monkeys.sort(key=lambda monkey: monkey.id_)

    return monkeys


def p1(data):
    monkeys = create_monkeys(data)

    for _ in range(20):
        for monkey in monkeys:
            for turn in monkey.take_turn():
                item, goes_to = turn
                monkeys[goes_to].items.append(item)

    inspection_counts = sorted(monkey.inspection_count for monkey in monkeys)
    return inspection_counts[-1] * inspection_counts[-2]


def p2(data):
    monkeys = create_monkeys(data)
    mod = reduce(lambda x, y: x * y, (monkey.div_test for monkey in monkeys))

    for _ in range(10000):
        for monkey in monkeys:
            for turn in monkey.take_turn(mod):
                item, goes_to = turn
                monkeys[goes_to].items.append(item)
        inspection_counts = [monkey.inspection_count for monkey in monkeys]

    inspection_counts = sorted(monkey.inspection_count for monkey in monkeys)
    return inspection_counts[-1] * inspection_counts[-2]
