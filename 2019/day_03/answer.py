def path_to_coords(path):
    start_co = (0, 0)
    coordinates = []

    diradders = {"U": (0, 1), "R": (1, 0), "D": (0, -1), "L": (-1, 0)}

    current_co = start_co
    for step in path:
        direction, distance = step[0], int(step[1:])
        for _ in range(distance):
            current_co = tuple(
                sum(x) for x in zip(current_co, diradders[direction])
            )
            coordinates.append(current_co)

    return coordinates


def p1(data, is_sample):
    wire1_path = data[0].split(",")
    wire2_path = data[1].split(",")

    wire1 = path_to_coords(wire1_path)
    wire2 = path_to_coords(wire2_path)

    intersections = set(wire1) & set(wire2)
    return min(sum(c) for c in intersections)


def p2(data, is_sample):
    wire1_path = data[0].split(",")
    wire2_path = data[1].split(",")

    wire1 = path_to_coords(wire1_path)
    wire2 = path_to_coords(wire2_path)

    intersections = set(wire1) & set(wire2)

    intersection_steps = set()
    for intersection in intersections:
        steps1 = wire1.index(intersection) + 1
        steps2 = wire2.index(intersection) + 1
        intersection_steps.add(steps1 + steps2)

    return min(intersection_steps)
