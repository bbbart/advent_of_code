def inc_cycle(cycle, checked_values, reg_x):
    new_cycle = cycle + 1
    if (new_cycle - 20) % 40 == 0:
        checked_values.append((new_cycle, reg_x))
    return new_cycle


def draw_pixel(crt_pos, reg_x):
    rel_pos = crt_pos % 40
    if rel_pos == 0:
        print()
    if abs(rel_pos - reg_x) < 2:
        print("#", end="")
    else:
        print(".", end="")


def p1(data, is_sample):
    cycle = 0
    reg_x = 1

    checked_values = []

    for instruction in data:
        if instruction.startswith("noop"):
            cycle = inc_cycle(cycle, checked_values, reg_x)
        elif instruction.startswith("addx"):
            cycle = inc_cycle(cycle, checked_values, reg_x)
            cycle = inc_cycle(cycle, checked_values, reg_x)

            value = int(instruction.split()[-1])
            reg_x += value

    return sum(map(lambda val: val[0] * val[1], checked_values))


def p2(data, is_sample):
    cycle = 0
    reg_x = 1
    crt_pos = 0

    for instruction in data:
        if instruction.startswith("noop"):
            cycle += 1
            draw_pixel(crt_pos, reg_x)
            crt_pos += 1
        elif instruction.startswith("addx"):
            cycle += 1
            draw_pixel(crt_pos, reg_x)
            crt_pos += 1

            cycle += 1
            draw_pixel(crt_pos, reg_x)
            crt_pos += 1

            value = int(instruction.split()[-1])
            reg_x += value

    print()
