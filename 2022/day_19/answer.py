import re
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum


class Resource(Enum):
    ORE = "ore"
    CLAY = "clay"
    OBSIDIAN = "obsidian"
    GEODE = "geode"

    def __lt__(self, other):
        return list(Resource.__members__.values()).index(self) < list(
            Resource.__members__.values()
        ).index(other)


@dataclass
class Blueprint:
    id_: int
    costs: dict[Resource, int]


class Wallet(dict):
    def pay(self, price: dict):
        for resource, amount in price.items():
            self[resource] -= amount

    def receive(self, price: dict):
        for resource, amount in price.items():
            self[resource] += amount

    def can_afford(self, price: dict):
        return all(
            self[resource] >= amount for resource, amount in price.items()
        )

    def __str__(self):
        return "You have " + ", ".join(
            f"{amount} {resource.value}" for resource, amount in self.items()
        )


def how_long_before_i_can_afford(
    blueprint: Blueprint,
    wallet: Wallet,
    robots: dict[Resource, int],
    product: Resource,
):
    pretend_wallet = deepcopy(wallet)
    rounds = 0
    while not pretend_wallet.can_afford(blueprint.costs[product]):
        if not set(blueprint.costs[product]).issubset(set(robots)):
            return -1
        for resource, collection in robots.items():
            pretend_wallet.receive({resource: collection})
        rounds += 1
    return rounds


def parse_cost(cost: str):
    costre = re.compile(rf"\d+ (?:{'|'.join(r.value for r in Resource)})")
    costs = map(lambda s: s.split(), costre.findall(cost))
    return {Resource(name): int(amount) for amount, name in costs}


def get_blueprints(data):
    for line in data:
        (
            id_,
            cost_orerobot,
            cost_clayrobot,
            cost_obsidianrobot,
            cost_geoderobot,
        ) = re.match(
            r"Blueprint (\d+): Each ore robot costs (.+?)\. "
            r"Each clay robot costs (.+?)\. "
            r"Each obsidian robot costs (.+?)\. "
            r"Each geode robot costs (.+?)\.",
            line,
        ).groups()

        yield Blueprint(
            int(id_),
            {
                Resource.ORE: parse_cost(cost_orerobot),
                Resource.CLAY: parse_cost(cost_clayrobot),
                Resource.OBSIDIAN: parse_cost(cost_obsidianrobot),
                Resource.GEODE: parse_cost(cost_geoderobot),
            },
        )


def p1(data, is_sample):
    blueprints = get_blueprints(data)

    quality_level = 0
    for blueprint in blueprints:
        wallet = Wallet({resouce: 0 for resouce in Resource})
        robots: dict[Resource, int] = defaultdict(int)
        robots[Resource.ORE] = 1
        robots_needed = {Resource.GEODE}
        for _ in range(24):
            # plan
            while True:
                planned_robot = sorted(robots_needed)[0]
                time_needed = how_long_before_i_can_afford(
                    blueprint, wallet, robots, planned_robot
                )
                can_be_planned = time_needed != -1

                if not can_be_planned:
                    extra_robots_needed = set(
                        blueprint.costs[planned_robot]
                    ) - set(robots)
                    robots_needed ^= extra_robots_needed
                else:
                    if planned_robot == min(Resource):
                        break
                    # NOT GOOD ENOUGH...
                    break

            # buy
            in_production = None
            if wallet.can_afford(blueprint.costs[planned_robot]):
                wallet.pay(blueprint.costs[planned_robot])
                if planned_robot != Resource.GEODE:
                    robots_needed.remove(planned_robot)
                in_production = planned_robot

            # collect
            for resource, collection in robots.items():
                wallet.receive({resource: collection})

            # produce
            if in_production:
                robots[in_production] += 1

        quality_level += blueprint.id_ * wallet[Resource.GEODE]

    return quality_level
