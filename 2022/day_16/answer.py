import re
from collections import defaultdict
from dataclasses import dataclass


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


class KaBoom(Exception):
    pass


class Cave:
    def __init__(
        self,
        valves: list[Valve],
        network: dict[str, str],
        starting_position: str,
    ):
        self._valves = {valve.name: valve for valve in valves}
        self.network = network
        self.current_position = starting_position
        self._minutes_before_eruption: int = 30
        self.pressure_released = 0

        self.max_flow = max(valve.flow_rate for valve in valves)

    @property
    def loneliness(self):
        loneliness_score = defaultdict(int)
        for valve_from in self._valves.values():
            for valve_to in self._valves.values():
                if valve_from == valve_to:
                    continue
                shortest_path = self.shortest_path(
                    valve_from.name, valve_to.name
                )
                if valve_to.closed:
                    loneliness_score[valve_from.name] += (
                        len(shortest_path) - 1
                    ) * (self.max_flow - valve_to.flow_rate)
        return loneliness_score

    @property
    def open_valves(self):
        return filter(lambda valve: valve.opened, self._valves.values())

    @property
    def closed_valves(self):
        return filter(lambda valve: valve.closed, self._valves.values())

    @property
    def valves_to_open(self):
        return filter(lambda valve: valve.flow_rate > 0, self.closed_valves)

    @property
    def has_valves_to_open(self):
        return bool(list(self.valves_to_open))

    @property
    def current_release(self):
        return sum(valve.flow_rate for valve in self.open_valves)

    def tick_clock(self, amount: int = 1):
        for _ in range(amount):
            if self._minutes_before_eruption <= 1:
                raise KaBoom
            self.pressure_released += self.current_release
            self._minutes_before_eruption -= 1

    def shortest_path(self, fr: str, to: str):
        path_list = [[fr]]
        path_index = 0
        # To keep track of previously visited nodes
        previous_nodes = {fr}
        if fr == to:
            return path_list[0]

        while path_index < len(path_list):
            current_path = path_list[path_index]
            last_node = current_path[-1]
            next_nodes = self.network[last_node]
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

    def move_to(self, target_position: str):
        path = self.shortest_path(self.current_position, target_position)
        self.tick_clock(len(path) - 1)
        self.current_position = target_position

    def open_valve(self, valve: str):
        self._valves[valve].open()
        self.tick_clock(1)

    def yield_if_moved_to_and_opened(self, target_valve: str):
        path = self.shortest_path(self.current_position, target_valve)
        time_remaining_after_opening = self._minutes_before_eruption - len(
            path
        )
        return (
            time_remaining_after_opening * self._valves[target_valve].flow_rate
        )

    def __str__(self):
        state = (
            f"Time left: {self._minutes_before_eruption} minutes.\n"
            f"Currently opened valves: {', '.join(map(lambda v: v.name,self.open_valves))}.\n"
            f"{self.current_release} pressure is currently being released per minute.\n"
            f"{self.pressure_released} pressure has been released in total until now.\n"
            f"You are at {self.current_position}."
        )
        return state


def p1(data, is_sample=False):
    # create valves and build graph
    graph: dict[str, list] = defaultdict(list)
    valves: list[Valve] = []
    for line in data:
        target_valve_name, flow_rate, connections = re.match(
            r"Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)",
            line,
        ).groups()

        target_valve = Valve(target_valve_name, int(flow_rate))
        valves.append(target_valve)
        graph[target_valve_name] = connections.split(", ")

    cave = Cave(valves, graph, "AA")

    path = ["AA"]
    try:
        while cave.has_valves_to_open:
            score = defaultdict(int)
            for valve_to in cave.valves_to_open:
                score[valve_to.name] = (
                    cave.yield_if_moved_to_and_opened(valve_to.name)
                    # - cave.loneliness[valve_to.name]
                )

            print(score)
            target = sorted(score.items(), key=lambda v: v[1])[-1][0]
            path.append(target)

            cave.move_to(target)
            cave.open_valve(target)
        while True:
            cave.tick_clock()
    except KaBoom:
        print(path)
        return cave.pressure_released
