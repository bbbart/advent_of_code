from copy import deepcopy
from itertools import permutations
from queue import SimpleQueue


# pylint: disable=too-many-branches,too-many-statements
# I want to keep the intcode computer code in one 'simple' function.
def intcode_p1(instructions, inputlist: list):
    parameters = iter(inputlist)
    pointer = 0

    output = []
    while True:
        instruction = str(instructions[pointer]).zfill(5)
        opcode = int(instruction[-2:])
        if opcode == 1:  # ADD
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            res_pos = instructions[pointer + 3]
            instructions[res_pos] = param1 + param2

            pointer += 4
        elif opcode == 2:  # MULTIPLY
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            res_pos = instructions[pointer + 3]
            instructions[res_pos] = param1 * param2

            pointer += 4
        elif opcode == 3:  # INPUT
            value = int(next(parameters))
            # value = int(input('value> '))
            instructions[instructions[pointer + 1]] = value

            pointer += 2
        elif opcode == 4:  # OUTPUT
            value = instructions[instructions[pointer + 1]]
            output.append(value)

            pointer += 2
        elif opcode == 5:  # JUMP-IF-TRUE
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            if param1:
                pointer = param2
            else:
                pointer += 3
        elif opcode == 6:  # JUMP-IF-FALSE
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            if not param1:
                pointer = param2
            else:
                pointer += 3
        elif opcode == 7:  # LESS THAN
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            res_pos = instructions[pointer + 3]
            if param1 < param2:
                instructions[res_pos] = 1
            else:
                instructions[res_pos] = 0

            pointer += 4
        elif opcode == 8:  # EQUALS
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            res_pos = instructions[pointer + 3]
            if param1 == param2:
                instructions[res_pos] = 1
            else:
                instructions[res_pos] = 0

            pointer += 4
        elif opcode == 99:
            return instructions, output, pointer
        else:
            print(f"ERROR: unknown opcode {opcode}")


# pylint: disable=too-many-branches,too-many-statements
# I want to keep the intcode computer code in one 'simple' function.
def intcode_p2(instructions, inputqueue: SimpleQueue):
    pointer = 0

    while True:
        instruction = str(instructions[pointer]).zfill(5)
        opcode = int(instruction[-2:])
        if opcode == 1:  # ADD
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            res_pos = instructions[pointer + 3]
            instructions[res_pos] = param1 + param2

            pointer += 4
        elif opcode == 2:  # MULTIPLY
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            res_pos = instructions[pointer + 3]
            instructions[res_pos] = param1 * param2

            pointer += 4
        elif opcode == 3:  # INPUT
            try:
                value = inputqueue.get_nowait()
            except StopIteration:
                print("no enough inputs")
                return
            instructions[instructions[pointer + 1]] = value

            pointer += 2
        elif opcode == 4:  # OUTPUT
            value = instructions[instructions[pointer + 1]]
            yield value

            pointer += 2
        elif opcode == 5:  # JUMP-IF-TRUE
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            if param1:
                pointer = param2
            else:
                pointer += 3
        elif opcode == 6:  # JUMP-IF-FALSE
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            if not param1:
                pointer = param2
            else:
                pointer += 3
        elif opcode == 7:  # LESS THAN
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            res_pos = instructions[pointer + 3]
            if param1 < param2:
                instructions[res_pos] = 1
            else:
                instructions[res_pos] = 0

            pointer += 4
        elif opcode == 8:  # EQUALS
            if int(instruction[2]):
                param1 = instructions[pointer + 1]
            else:
                param1 = instructions[instructions[pointer + 1]]

            if int(instruction[1]):
                param2 = instructions[pointer + 2]
            else:
                param2 = instructions[instructions[pointer + 2]]

            res_pos = instructions[pointer + 3]
            if param1 == param2:
                instructions[res_pos] = 1
            else:
                instructions[res_pos] = 0

            pointer += 4
        elif opcode == 99:
            return
        else:
            print(f"ERROR: unknown opcode {opcode}")
            return


def p1(data, is_sample):
    if is_sample:
        return "N/A"

    source = list(map(int, data[0].split(",")))
    phase_settings = permutations(range(5))

    signal = 0
    for settings in phase_settings:
        ampa_output = intcode_p1(deepcopy(source), [settings[0], 0])
        ampb_output = intcode_p1(
            deepcopy(source), [settings[1], ampa_output[1][0]]
        )
        ampc_output = intcode_p1(
            deepcopy(source), [settings[2], ampb_output[1][0]]
        )
        ampd_output = intcode_p1(
            deepcopy(source), [settings[3], ampc_output[1][0]]
        )
        ampe_output = intcode_p1(
            deepcopy(source), [settings[4], ampd_output[1][0]]
        )
        signal = max(signal, ampe_output[1][0])

    return signal


def p2(data, is_sample):
    phase_settings = permutations(range(5, 10))
    signal = 0

    for settings in phase_settings:
        source = list(map(int, data[0].split(",")))

        # queues to channel output from one amp to input for another one
        queues = [
            SimpleQueue(),
            SimpleQueue(),
            SimpleQueue(),
            SimpleQueue(),
            SimpleQueue(),
        ]

        # set the phase settings as inputs
        for q, s in zip(queues, settings):
            q.put_nowait(s)
        # set the initial input for amp A to 0
        queues[0].put_nowait(0)

        # create the amps
        amps = []
        for q in queues:
            amps.append(intcode_p2(deepcopy(source), q))

        # and start the feedback loop
        while True:
            try:
                for q, a in zip(queues[1:] + [queues[0]], amps):
                    q.put_nowait(next(a))
            except StopIteration:
                # when we're done, get the final output of the last amp (set in
                # the first queue)
                signal = max(signal, queues[0].get_nowait())
                break

    return signal
