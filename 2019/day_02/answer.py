def p1(data, is_sample):
    data = list(map(int, data[0].split(",")))
    if not is_sample:
        data[1] = 12
        data[2] = 2
    for line, opcode in enumerate(data[::4]):
        term1_pos = data[4 * line + 1]
        term2_pos = data[4 * line + 2]
        res_pos = data[4 * line + 3]
        if opcode == 1:
            data[res_pos] = data[term1_pos] + data[term2_pos]
        elif opcode == 2:
            data[res_pos] = data[term1_pos] * data[term2_pos]
        elif opcode == 99:
            return data[0]
        else:
            print(f"ERROR: unknown opcode {opcode}")


def p2(data, is_sample):
    if is_sample:
        return "N/A"

    data = list(map(int, data[0].split(",")))

    # the total equation is:
    #   result = 320000 * noun + 1450679 + verb
    # so we need to solve this equation for 19690720
    # with both noun and verb <= len(data)
    #   19690720 = 320000 * noun + 1450679 + verb
    #   => 0 = 320000 * noun + verb - 18240041
    #   => noun = 57, verb = 41

    noun = 57
    verb = 41

    if not is_sample:
        data[1] = noun
        data[2] = verb

    for line, opcode in enumerate(data[::4]):
        term1_pos = data[4 * line + 1]
        term2_pos = data[4 * line + 2]
        res_pos = data[4 * line + 3]
        if opcode == 1:
            data[res_pos] = data[term1_pos] + data[term2_pos]
        elif opcode == 2:
            data[res_pos] = data[term1_pos] * data[term2_pos]
        elif opcode == 99:
            if data[0] == 19690720:
                return 100 * noun + verb
            return f"FAIL ({data[0]})"
        else:
            print(f"ERROR: unknown opcode {opcode}")
