#!/usr/bin/env python

import re

re_workflow = re.compile(r"(?P<name>.*){(?P<conditions>.*)}")
re_rule = re.compile(
    r"((?P<category>.)(?P<comparator>[<>])(?P<threshold>\d+):)?(?P<target>.*)"
)


def rule_to_def(rulestring) -> callable:
    match = re_rule.match(rulestring)
    assert match
    if match["comparator"]:
        # pylint: disable=consider-using-f-string
        # This is cleaner.
        comp = "part['%s'] %s %d" % (
            match["category"],
            match["comparator"],
            int(match["threshold"]),
        )

        def ruledef(part):
            # pylint: disable=eval-used
            # I want to avoid sympy and this is just quick...
            # I feel 'protected' by the asserting the re matches above
            return match["target"] if eval(comp) else None

    else:

        def ruledef(part):
            return match["target"]

    return ruledef


def p1(data, is_sample):
    workflows = {}
    parts = []
    workflow_or_part = False
    for line in data:
        if not line:
            workflow_or_part = True
            continue
        if not workflow_or_part:
            # workflow
            name, rulestring = re_workflow.match(line).groups()
            workflows[name] = [rule_to_def(r) for r in rulestring.split(",")]
        else:
            # part
            part = {}
            for m in re.finditer(r"(?P<xmas>[xmas])=(?P<value>\d+)", line):
                part[m["xmas"]] = int(m["value"])
            parts.append(part)

    ans = 0
    for part in parts:
        workflow = "in"
        more = True
        while more:
            rules = workflows[workflow]
            for rule in rules:
                workflow = rule(part)

                if not workflow:
                    continue

                if workflow == "A":
                    ans += sum(part.values())

                more = not workflow in ("A", "R")
                break

    return ans


def p2(data, is_sample):
    workflows = {}
    for line in data:
        if not line:
            break
        name, rulestring = re_workflow.match(line).groups()
        workflows[name] = rulestring.split(",")

    # now we need to simplify the workflows. using the sample input, for
    # example, it can be shown that if s > 2778, the part is automatically
    # accepted, regardless of the values for x, m and a.

    def invert(rule):
        if "<" in rule:
            return rule.replace("<", ">=").split(":")[0]

        if ">" in rule:
            return rule.replace(">", "<=").split(":")[0]

        return rule

    # DFS to find all paths from `in` to `A`
    def accflows(start, aggflow):
        if start == "R":
            return

        if start == "A":
            yield aggflow + [start]
            return

        rules = workflows[start]
        for i in range(len(rules)):
            if i:
                aggflow[-1] = invert(workflows[start][i - 1])
            rule = workflows[start][i]
            try:
                lhs, rhs = rule.split(":")
            except ValueError:
                lhs = ""
                rhs = rule
            if lhs:
                aggflow.append(lhs)
            yield from accflows(rhs, aggflow[:])

    re_comp = re.compile(r"(?P<xmas>[xmas])(?P<comp>[<>]=?)(?P<value>\d+)")
    accepted_parts = 0
    for accepted_flow in accflows("in", []):
        xmas = {
            "x": {"min": 1, "max": 4000},
            "m": {"min": 1, "max": 4000},
            "a": {"min": 1, "max": 4000},
            "s": {"min": 1, "max": 4000},
        }
        for rule in accepted_flow[:-1]:
            char, comp, val = re.match(re_comp, rule).groups()
            if comp == "<":
                xmas[char]["max"] = min(int(val) - 1, xmas[char]["max"])
            elif comp == "<=":
                xmas[char]["max"] = min(int(val), xmas[char]["max"])
            elif comp == ">":
                xmas[char]["min"] = max(int(val) + 1, xmas[char]["min"])
            elif comp == ">=":
                xmas[char]["min"] = max(int(val), xmas[char]["min"])

        ran = 1
        for char in "xmas":
            ran *= xmas[char]["max"] - xmas[char]["min"] + 1
        accepted_parts += ran

    return accepted_parts
