#!/usr/bin/env python

from collections import namedtuple
from dataclasses import dataclass, field
from math import lcm
from queue import Empty, SimpleQueue

Signal = namedtuple("Signal", ("hilo", "source", "sink"))


@dataclass
class Module:
    type_: chr
    destinations: list["Module"]

    def process_signal(self, signal: Signal) -> bool | None:
        return signal.hilo


# pylint: disable=too-few-public-methods
class FlipFlop(Module):
    state: bool = False

    def process_signal(self, signal: Signal) -> bool | None:
        if signal.hilo:
            return None
        self.state = not self.state
        return self.state


# pylint: disable=too-few-public-methods
class Conjunction(Module):
    pulse_memory: dict[str, bool] = field(default_factory=dict)

    def process_signal(self, signal: Signal) -> bool | None:
        self.pulse_memory[signal.source] = signal.hilo
        return not all(self.pulse_memory.values())


def parse_input(data):
    # define modules
    modules = {}
    for line in data:
        label, destinations = line.split(" -> ")
        if label.startswith("%"):
            module_type = "f"  # flip-flop
            name = label[1:]
            module = FlipFlop(module_type, destinations.split(", "))
        elif label.startswith("&"):
            module_type = "c"  # conjunction
            name = label[1:]
            module = Conjunction(module_type, destinations.split(", "))
            module.pulse_memory = {}
        else:
            module_type = "b"  # broadcaster
            name = label
            module = Module(module_type, destinations.split(", "))

        modules[name] = module

    # initialize conjunction modules
    for name, module in modules.items():
        for d in module.destinations:
            dest = modules.get(d, None)
            if isinstance(dest, Conjunction):
                dest.pulse_memory[name] = False

    return modules


def p1(data, is_sample):
    modules = parse_input(data)

    signal_count = {True: 0, False: 0}
    signals = SimpleQueue()
    for _ in range(1000):
        signals.put(Signal(False, "button", "broadcaster"))
        signal_count[False] += 1

        while True:
            try:
                signal = signals.get_nowait()
            except Empty:
                break

            try:
                hilo = modules[signal.sink].process_signal(signal)
            except KeyError:
                # this sink module is untyped
                hilo = None

            if hilo is None:
                continue

            for d in modules[signal.sink].destinations:
                signals.put(Signal(hilo, signal.sink, d))
                signal_count[hilo] += 1

    return signal_count[True] * signal_count[False]


def p2(data, is_sample):
    if is_sample:
        return "N/A"

    modules = parse_input(data)

    # we look at `xn`, since that is the only module outputting to `rx`.
    # this is a conjunction module, so we need to know when all of it's pulse
    # memory entries are True
    #
    # since this is necessarily cyclical, we just register when each of them
    # switches to True individually and calculate the lcm of those counts
    xn_mem = {source: 0 for source in modules["xn"].pulse_memory.keys()}

    button_presses = 0
    signals = SimpleQueue()
    while True:
        signals.put(Signal(False, "button", "broadcaster"))
        button_presses += 1

        while True:
            try:
                signal = signals.get_nowait()
                if signal.sink == "rx" and not signal.hilo:
                    return button_presses
            except Empty:
                break

            try:
                hilo = modules[signal.sink].process_signal(signal)
            except KeyError:
                # this sink module is untyped
                hilo = None

            if hilo is None:
                continue

            for d in modules[signal.sink].destinations:
                signals.put(Signal(hilo, signal.sink, d))
                for mod, mem in modules["xn"].pulse_memory.items():
                    if mem and not xn_mem[mod]:
                        xn_mem[mod] = button_presses
                    if all(xn_mem.values()):
                        return lcm(*xn_mem.values())
