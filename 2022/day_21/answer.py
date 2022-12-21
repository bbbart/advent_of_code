from sympy import sympify
from sympy.solvers import solve


def p1(data, is_sample):
    equalities = {}
    for line in data:
        left, right = line.split(": ")
        try:
            right = int(right)
            equalities[left] = right
        except ValueError:
            right = sympify(right)
            equalities[left] = right

    substitution = equalities["root"].subs(equalities)
    while True:
        try:
            return int(substitution)
        except TypeError:
            substitution = substitution.subs(equalities)


def p2(data, is_sample):
    equalities = {}
    for line in data:
        left, right = line.split(": ")
        if left == "root":
            to_equalize = (right[:4], right[-4:])
            continue
        if left == "humn":
            continue
        try:
            right = int(right)
            equalities[left] = right
        except ValueError:
            right = sympify(right)
            equalities[left] = right

    substitutions = {}
    for to_solve in to_equalize:
        substitution = equalities[to_solve].subs(equalities)
        while True:
            if len(substitution.free_symbols) <= 1:
                substitutions[to_solve] = substitution
                break
            substitution = substitution.subs(equalities)

    equations = list(substitutions.values())
    return solve(equations[1] - equations[0], "humn")[0]
