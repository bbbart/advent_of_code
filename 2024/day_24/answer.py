#!/usr/bin/env python

import re
import sys
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class AND:
    in1: str
    in2: str
    out: str
    in1_val: int = 0
    in2_val: int = 0

    @property
    def out_val(self) -> int:
        return self.in1_val & self.in2_val

    def __hash__(self):
        return hash((self.in1, self.in2, self.out))

    def __repr__(self):
        return f"{self.in1} AND {self.in2} -> {self.out}"


@dataclass
class OR:
    in1: str
    in2: str
    out: str
    in1_val: int = 0
    in2_val: int = 0

    @property
    def out_val(self) -> int:
        return self.in1_val | self.in2_val

    def __hash__(self):
        return hash((self.in1, self.in2, self.out))

    def __repr__(self):
        return f"{self.in1} AND {self.in2} -> {self.out}"


@dataclass
class XOR:
    in1: str
    in2: str
    out: str
    in1_val: int = 0
    in2_val: int = 0

    @property
    def out_val(self) -> int:
        return self.in1_val ^ self.in2_val

    def __hash__(self):
        return hash((self.in1, self.in2, self.out))

    def __repr__(self):
        return f"{self.in1} AND {self.in2} -> {self.out}"


def p1(data: list[str], is_sample: bool):
    wires: dict[str, int] = {}
    gates = set()
    for line in data:
        if m := re.match(r"^(.+): ([01])$", line):
            wires[m.group(1)] = int(m.group(2))
        elif m := re.match(r"^(.+) (AND|XOR|OR) (.+) -> (.+)$", line):
            gate_class = getattr(sys.modules[__name__], m.group(2))
            gates.add(gate_class(m.group(1), m.group(3), m.group(4)))

    while gates:
        gate = gates.pop()
        try:
            gate.in1_val = wires[gate.in1]
            gate.in2_val = wires[gate.in2]
            wires[gate.out] = gate.out_val
        except KeyError:
            gates.add(gate)

    bits = ""
    for wire in sorted(
        filter(lambda w: w.startswith("z"), wires), reverse=True
    ):
        bits += str(wires[wire])

    return int(bits, 2)


def p2(data: list[str], is_sample: bool):
    return "N/A"

    wires = {}
    gates = set()
    for line in data:
        if m := re.match(r"^(?P<wire>.+): (?P<value>[01])$", line):
            wires[m["wire"]] = int(m["value"])
        elif m := re.match(
            r"^(?P<in1>.+) (?P<logic>AND|XOR|OR) (?P<in2>.+) -> (?P<out>.+)$",
            line,
        ):
            gate_class = getattr(sys.modules[__name__], m.group(2))
            gates.add(gate_class(m["in1"], m["in2"], m["out"]))

    def visualise(gates):
        with open("/tmp/gates.dot", "w", encoding="utf-8") as dotfile:
            shapes = {
                "AND": "invtrapezium",
                "OR": "invtriangle",
                "XOR": "invhouse",
            }
            colours = {"AND": "red", "OR": "green", "XOR": "blue"}
            dotfile.write("digraph {\n")
            dotfile.write("node [shape=plaintext]\n")
            for gate in gates:
                dotfile.write(
                    f'"{gate}" [label="{gate.__class__.__name__}" shape={shapes[gate.__class__.__name__]} fillcolor={colours[gate.__class__.__name__]} style=filled];\n'
                )
                dotfile.write(f'{gate.in1} -> "{gate}";\n')
                dotfile.write(f'{gate.in2} -> "{gate}";\n')
                dotfile.write(f'"{gate}" -> {gate.out};\n')
            dotfile.write("}\n")

    def buildcircuit(gates):
        circuit = defaultdict(set)
        for gate in gates:
            circuit[gate.out].update((gate.in1, gate.in2))
        return circuit

    def runcircuit(x: int, y: int):
        x_wires = sorted(filter(lambda w: w.startswith("x"), wires))
        y_wires = sorted(filter(lambda w: w.startswith("y"), wires))

        tmpwires = wires.copy()
        for w, v in zip(
            x_wires, str(bin(x)[2:]).rjust(len(x_wires), "0")[::-1]
        ):
            tmpwires[w] = int(v)
        for w, v in zip(
            y_wires, str(bin(y)[2:]).rjust(len(y_wires), "0")[::-1]
        ):
            tmpwires[w] = int(v)

        tmpgates = gates.copy()
        while tmpgates:
            gate = tmpgates.pop()
            try:
                gate.in1_val = tmpwires[gate.in1]
                gate.in2_val = tmpwires[gate.in2]
                tmpwires[gate.out] = gate.out_val
            except KeyError:
                tmpgates.add(gate)

        bits = ""
        for wire in sorted(
            filter(lambda w: w.startswith("z"), tmpwires), reverse=True
        ):
            bits += str(tmpwires[wire])

        z = int(bits, 2)
        return (
            bin(x)[2:][-5:].rjust(5, "0"),
            bin(y)[2:][-5:].rjust(5, "0"),
            bits,
            f"{x} + {y} = {z}",
        )
        # return int(bits, 2)

    # gate1, gate2 = None, None
    # swaps = ((set((("y02", "y04"))), set((("x00", "y04")))),
    #          (set((("x01", "y02"))), set((("x00", "x01")))),
    #          )
    # for swap in swaps:
    #     for gate in gates.copy():
    #         if set((gate.in1, gate.in2)) == swap[0]:
    #             gate1 = gate
    #         if set((gate.in1, gate.in2)) == swap[1]:
    #             gate2 = gate
    #         if gate1 and gate2:
    #             break
    #     else:
    #         breakpoint()
    #     gate1.out, gate2.out = gate2.out, gate1.out

    circuit = buildcircuit(gates)

    # investigation teaches us (for input_sample):
    # 00000 + 00000 -> 0000000000000
    # 00000 + 00001 -> 1001000000010
    # 00001 + 00000 -> 0010111110000
    # 00001 + 00001 -> 1011111110010
    # 11111 + 11111 -> 1110111110010
    # x00 and y00 should only ever impact z00 (xor) and z01 (and)

    impacted_by: dict[str, set[str]] = defaultdict(set)
    for wire in filter(lambda w: w.startswith("z"), sorted(circuit)):
        print()
        visited = set()
        queue = [(wire, [wire])]
        while queue:
            current, path = queue.pop()
            if current.startswith("x") or current.startswith("y"):
                print(path)
            if current in visited:
                continue
            visited.add(current)
            for w in circuit[current]:
                queue.append((w, path + [w]))
        impacted_by[wire] = tuple(
            filter(lambda w: w.startswith("x") or w.startswith("y"), visited)
        )

    # this tells us:
    # z00 is impacted by x00, x01,      x03,                y02,      y04
    # z01                x00,           x03, x04, y00,      y02, y03, y04
    # z02                     x01, x02,                y01, y02, y03, y04
    # z03                x00, x01,      x03,                     y03
    # z04                x00, x01, x02, x03,      y00, y01, y02, y03
    # z05                x00,      x02,      x04, y00, y01,      y03, y04
    # z06                x00, x01,      x03,                y02, y03
    # z07                x00, x01,      x03,                y02, y03, y04
    # z08                x00, x01,      x03,                y02, y03
    # z09                          x02,           y00, y01, y02, y03, y04
    # z10                x00, x01,      x03,                y02
    # z11                     x01, x02,           y00, y01, y02, y03, y04
    # z12                x00,           x03, x04, y00,      y02, y03, y04

    # x00 impacts z00, z01,      z03, z04, z05, z06, z07, z08,      z10,      z12
    # x01 impacts z00,      z02, z03, z04,      z06, z07, z08,      z10, z11
    # x02 impacts           z02,      z04, z05,                z09,      z11
    # x03 impacts z00, z01,      z03, z04,      z06, z07, z08,      z10,      z12
    # x04 impacts      z01,                z05,                               z12
    # y00 impacts      z01,           z04, z05,                z09,      z11, z12
    # y01 impacts           z02,      z04, z05,                z09,      z11
    # y02 impacts z00, z01, z02,      z04,      z06, z07, z08, z09, z10, z11  z12
    # y03 impacts      z01, z02, z03, z04, z05, z06, z07, z08, z09,      z11, z12
    # y04 impacts z00, z01, z02,           z05,      z07,      z09,      z11, z12

    print()
    print(runcircuit(0, 0))
    print(runcircuit(0, 1))
    print(runcircuit(1, 0))
    print(runcircuit(1, 1))
