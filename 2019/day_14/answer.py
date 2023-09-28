from collections import defaultdict


def p1(data, is_sample):
    reactions: dict[tuple[tuple[int, str]], tuple[int, str]] = {}

    for line in data:
        chem_in, chem_out = line.split(" => ")
        chems_in = chem_in.split(", ")
        key = tuple(
            tuple(map(lambda x, f: f(x), ci.split(" "), [int, str]))
            for ci in chems_in
        )
        reactions[key] = tuple(
            map(lambda x, f: f(x), chem_out.split(" "), [int, str])
        )

    have: dict[str, int] = defaultdict(int)
    need: dict[str, int] = defaultdict(int)

    need["FUEL"] = 1
    while True:
        new_needs: dict[str, int] = defaultdict(int)
        for chemical, amount in need.items():
            if chemical == "ORE":
                continue

            if have[chemical] >= amount:
                continue

            for chem_in, chem_out in reactions.items():
                if chemical not in chem_out:
                    continue
                for amount, chem in chem_in:
                    new_needs[chem] += amount
                have[chem_out[1]] += chem_out[0]
                break

        if not new_needs:
            return need["ORE"]

        for chem, amount in new_needs.items():
            need[chem] += amount


def p2(data, is_sample):
    reactions: dict[tuple[tuple[int, str]], tuple[int, str]] = {}

    for line in data:
        chem_in, chem_out = line.split(" => ")
        chems_in = chem_in.split(", ")
        chem_out_amount, chem_out_chem = chem_out.split(" ")
        reactions[chem_out_chem] = (
            int(chem_out_amount),
            {
                chem: int(amount)
                for amount, chem in (ci.split(" ") for ci in chems_in)
            },
        )

    def get_ore_requirement(chemical, amount_needed, reactions, leftovers):
        if chemical == "ORE":
            return amount_needed

        total_ore = 0

        # use leftovers first if available
        if chemical in leftovers:
            from_leftover = min(leftovers[chemical], amount_needed)
            amount_needed -= from_leftover
            leftovers[chemical] -= from_leftover

        # if we still need more, then produce it
        if amount_needed > 0:
            produced_amount, reaction = reactions[chemical]
            batches_needed = amount_needed // produced_amount
            leftover_amount = batches_needed * produced_amount - amount_needed

            for sub_chemical, sub_amount in reaction.items():
                total_ore += get_ore_requirement(
                    sub_chemical,
                    sub_amount * batches_needed,
                    reactions,
                    leftovers,
                )

            # store the leftover amount
            if leftover_amount > 0:
                leftovers[chemical] += leftover_amount

        return total_ore

    leftovers = defaultdict(int)
    lets_try = 1
    too_little = None
    too_much = None

    while True:
        ore_needed = get_ore_requirement("FUEL", lets_try, reactions, leftovers)
        if ore_needed < 1000000000000:
            too_little = lets_try
        elif ore_needed > 1000000000000:
            too_much = lets_try
        else:
            return lets_try

        if too_much and too_little:
            if abs(too_much - too_little) < 2:
                return too_little
            lets_try = too_little + (too_much - too_little) // 2  # bifurcate
        elif not too_much:
            lets_try = too_little * 2
        else:
            lets_try = too_much // 2
