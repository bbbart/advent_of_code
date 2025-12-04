#!/usr/bin/env python

import re
import sys

# SOLUTION (18216) IS WRONG, BUT NO TIME TO DEBUG...

class Group:
    def __init__(
        self,
        units: int,
        hit_points: int,
        weaknesses: tuple[str],
        immunities: tuple[str],
        damage_points: int,
        damage_type: str,
        initiative: int,
    ):
        self._units = units
        self.hit_points = hit_points
        self._weaknesses = weaknesses
        self._immunities = immunities
        self._damage_points = damage_points
        self.damage_type = damage_type
        self.initiative = initiative

    def __repr__(self):
        return f"Group({self.units}, {self.hit_points}, {self.initiative})"

    @property
    def effective_power(self):
        return self._units * self._damage_points

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value

    def damaged_by(self, other: "Group"):
        if other.damage_type in self._immunities:
            return 0
        if other.damage_type in self._weaknesses:
            return 2 * other.effective_power
        return other.effective_power


GROUP_RE = re.compile(
    r"(?P<units>\d+) units each with (?P<hit_points>\d+) hit points (?P<wai>\(.*\) )?with an attack that does (?P<damage_points>\d+) (?P<damage_type>\w+) damage at initiative (?P<initiative>\d+)"
)


def p1(data: list[str], is_sample: bool):
    # parse input
    immune_system = set()
    infection = set()
    for line in data:
        if not line:
            continue
        if not line[0].isdigit():
            if line == "Immune System:":
                army = immune_system
            elif line == "Infection:":
                army = infection
            else:
                print("UNKNOWN ARMY NAME")
                sys.exit(1)
            continue
        match = GROUP_RE.match(line)
        if not match:
            print("UNPARESABLE GROUP")
            sys.exit(1)

        weaknesses, immunities = (), ()
        if match["wai"]:
            for wai in map(str.strip, match.group("wai")[1:-2].split(";")):
                if wai.startswith("weak"):
                    weaknesses = tuple(map(str.strip, wai[8:].split(",")))
                elif wai.startswith("immune"):
                    immunities = tuple(map(str.strip, wai[10:].split(",")))

        group = Group(
            int(match["units"]),
            int(match["hit_points"]),
            weaknesses,
            immunities,
            int(match["damage_points"]),
            match["damage_type"],
            int(match["initiative"]),
        )
        army.add(group)

    def fight(army1, army2):
        def target_selection(attackers, defenders):
            for g in sorted(
                attackers, key=lambda g: (g.effective_power, g.initiative), reverse=True
            ):
                if not g.units:
                    continue
                target = max(
                    defenders,
                    key=lambda h: (h.damaged_by(g), h.effective_power, h.initiative),
                )
                defenders.remove(target)
                yield (g, target)
                if not defenders:
                    return

        # for army in army1, army2:
        #     for group in army:
        #         print(group.units)
        #     print()
        # print("---")

        # PHASE: target selection
        battles = list(target_selection(army1, army2.copy())) + list(
            target_selection(army2, army1.copy())
        )

        # PHASE: attacking
        for battle in sorted(battles, key=lambda b: b[0].initiative, reverse=True):
            attacker, defender = battle
            if not defender.units:
                continue
            damage = defender.damaged_by(attacker)
            defender.units = max(0, defender.units - damage // defender.hit_points)

        # PHASE: cleanup
        for army in army1, army2:
            for group in army.copy():
                if not group.units:
                    army.remove(group)

    while immune_system and infection:
        fight(immune_system, infection)

    if immune_system:
        return sum(g.units for g in immune_system)
    else:
        return sum(g.units for g in infection)


def p2(data: list[str], is_sample: bool):
    if not is_sample:
        return "N/A"
    return "N/A"
