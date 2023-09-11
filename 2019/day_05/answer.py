def p1(data, is_sample):
    if is_sample:
        return "N/A"

    data = list(map(int, data[0].split(",")))

    output = []
    pointer = 0
    while True:
        instruction = str(data[pointer]).zfill(5)
        opcode = int(instruction[-2:])
        if opcode == 1:  # ADD
            if int(instruction[2]):
                param1 = data[pointer + 1]
            else:
                param1 = data[data[pointer + 1]]

            if int(instruction[1]):
                param2 = data[pointer + 2]
            else:
                param2 = data[data[pointer + 2]]

            res_pos = data[pointer + 3]
            data[res_pos] = param1 + param2

            pointer += 4
        elif opcode == 2:  # MULTIPLY
            if int(instruction[2]):
                param1 = data[pointer + 1]
            else:
                param1 = data[data[pointer + 1]]

            if int(instruction[1]):
                param2 = data[pointer + 2]
            else:
                param2 = data[data[pointer + 2]]

            res_pos = data[pointer + 3]
            data[res_pos] = param1 * param2

            pointer += 4
        elif opcode == 3:  # INPUT
            value = int(input('input> '))
            data[data[pointer + 1]] = value

            pointer += 2
        elif opcode == 4:  # OUTPUT
            value = data[data[pointer + 1]]
            output.append(value)

            pointer += 2
        elif opcode == 99:
            return output
        else:
            print(f"ERROR: unknown opcode {opcode}")


def p2(data, is_sample):
    data = list(map(int, data[0].split(",")))

    output = []
    pointer = 0
    while True:
        instruction = str(data[pointer]).zfill(5)
        opcode = int(instruction[-2:])
        if opcode == 1:  # ADD
            if int(instruction[2]):
                param1 = data[pointer + 1]
            else:
                param1 = data[data[pointer + 1]]

            if int(instruction[1]):
                param2 = data[pointer + 2]
            else:
                param2 = data[data[pointer + 2]]

            res_pos = data[pointer + 3]
            data[res_pos] = param1 + param2

            pointer += 4
        elif opcode == 2:  # MULTIPLY
            if int(instruction[2]):
                param1 = data[pointer + 1]
            else:
                param1 = data[data[pointer + 1]]

            if int(instruction[1]):
                param2 = data[pointer + 2]
            else:
                param2 = data[data[pointer + 2]]

            res_pos = data[pointer + 3]
            data[res_pos] = param1 * param2

            pointer += 4
        elif opcode == 3:  # INPUT
            value = int(input('input> '))
            data[data[pointer + 1]] = value

            pointer += 2
        elif opcode == 4:  # OUTPUT
            value = data[data[pointer + 1]]
            output.append(value)

            pointer += 2
        elif opcode == 5:  # JUMP-IF-TRUE
            if int(instruction[2]):
                param1 = data[pointer + 1]
            else:
                param1 = data[data[pointer + 1]]

            if int(instruction[1]):
                param2 = data[pointer + 2]
            else:
                param2 = data[data[pointer + 2]]

            if param1:
                pointer = param2
            else:
                pointer += 3
        elif opcode == 6:  # JUMP-IF-FALSE
            if int(instruction[2]):
                param1 = data[pointer + 1]
            else:
                param1 = data[data[pointer + 1]]

            if int(instruction[1]):
                param2 = data[pointer + 2]
            else:
                param2 = data[data[pointer + 2]]

            if not param1:
                pointer = param2
            else:
                pointer += 3
        elif opcode == 7:  # LESS THAN
            if int(instruction[2]):
                param1 = data[pointer + 1]
            else:
                param1 = data[data[pointer + 1]]

            if int(instruction[1]):
                param2 = data[pointer + 2]
            else:
                param2 = data[data[pointer + 2]]

            res_pos = data[pointer + 3]
            if param1 < param2:
                data[res_pos] = 1
            else:
                data[res_pos] = 0

            pointer += 4
        elif opcode == 8:  # EQUALS
            if int(instruction[2]):
                param1 = data[pointer + 1]
            else:
                param1 = data[data[pointer + 1]]

            if int(instruction[1]):
                param2 = data[pointer + 2]
            else:
                param2 = data[data[pointer + 2]]

            res_pos = data[pointer + 3]
            if param1 == param2:
                data[res_pos] = 1
            else:
                data[res_pos] = 0

            pointer += 4
        elif opcode == 99:
            return output
        else:
            print(f"ERROR: unknown opcode {opcode}")
