import re
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from itertools import permutations


@dataclass
class Route:
    path: list
    cost_to_move: int
    target_flow: int

    def __lt__(self, other):
        if self.cost_to_move == other.cost_to_move:
            return self.target_flow > other.target_flow
        return self.cost_to_move < other.cost_to_move


@dataclass
class Valve:
    name: str
    flow_rate: int
    opened: bool = False

    @property
    def closed(self):
        return not self.opened

    def open(self):
        self.opened = True


def cost_to_move(fr, to, minutes_left, valves):
    # the cost to move from valve fr to valve to is equal to the amount of
    # total pressure eventually NOT released because of time spent on moving
    # so the edge weight of the graph is changing depending on the
    #   - total time spent
    #   - state of its nodes (valves)
    # (doesn't know about the tunnel system, assumes the move is valid)
    unreleased_pressure = 0
    for valve in valves.values():
        if valve.closed:
            unreleased_pressure += valve.flow_rate

    return unreleased_pressure * minutes_left


def cost_to_follow(path, minutes_left, valves):
    total_cost = 0
    minutes_spent = 0
    for fr, to in pairwise(path):
        total_cost += cost_to_move(
            fr, to, minutes_left - minutes_spent, valves
        )
        minutes_spent += 1
    return total_cost


def shortest_path(graph, fr, to):
    path_list = [[fr]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {fr}
    if fr == to:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = graph[last_node]
        # Search goal node
        if to in next_nodes:
            current_path.append(to)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []


def calculate_total_release(path: list[str], graph: dict, valves: dict):
    total_time_spent = 0
    time_spent = 0
    total_release = 0
    current_valve = "AA"
    path = list(path)
    while total_time_spent < 30:
        currently_releasing = sum(
            valve.flow_rate for valve in valves.values() if valve.opened
        )
        if path:
            # find out where we travel to
            target_valve = path.pop(0)
            # calculate the time spent on travelling to and opening target valve
            time_spent = len(shortest_path(graph, current_valve, target_valve))
            # actually travel to the target valve
            current_valve = target_valve
            # open the target valve
            valves[target_valve].open()
        else:
            time_spent = 1
        # check our clock
        total_time_spent += time_spent

        total_release += time_spent * currently_releasing
    return total_release


def calculate_release(path, graph, valves, time_left):
    # how much will we be able to release if we follow the given path and open
    # the last valve
    time_to_walk_and_open = len(path)
    return (time_left - time_to_walk_and_open) * valves[path[-1]].flow_rate


def p1(data, is_sample=False):
    # create valves and build graph
    graph = defaultdict(list)
    valves = {}
    for line in data:
        target_valve_name, flow_rate, connections = re.match(
            r"Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)",
            line,
        ).groups()

        target_valve = Valve(target_valve_name, int(flow_rate))
        valves[target_valve_name] = target_valve
        graph[target_valve_name] = connections.split(", ")

    current_valve = "AA"
    time_remaining = 30
    while time_remaining > 0:
        target_evaluation = {}
        for target_valve in (
            valve
            for valve in valves.values()
            if valve.closed and valve.flow_rate != 0
        ):
            path = shortest_path(graph, current_valve, target_valve.name)
            total_release = calculate_release(
                path, graph, valves, time_remaining
            )
            target_evaluation[target_valve] = total_release
        best_target = sorted(target_evaluation.items(), key=lambda v: v[1])[
            -1
        ][0]
        print(best_target)
        time_remaining -= len(path)

    # # find the best course of action
    # paths = permutations(
    #     valve.name
    #     for valve in valves.values()
    #     if (valve.flow_rate != 0 and valve.name != "AA")
    # )

    # return max(
    #     calculate_total_release(path, graph, deepcopy(valves))
    #     for path in paths
    # )
