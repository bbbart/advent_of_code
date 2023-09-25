from collections import defaultdict
from queue import SimpleQueue


# pylint: disable=too-many-branches,too-many-statements,too-many-locals
def intcode(instructions, inputqueue: SimpleQueue):

    memory = defaultdict(int)
    for address, value in enumerate(instructions):
        memory[address] = value

    # describes how the parameters work for the different opcodes:
    #   0: read parameter
    #   1: write paremter (can never be in immesdiate mode)
    param_types: dict[int, int] = {
        1: (0, 0, 1),  # ADD
        2: (0, 0, 1),  # MULTIPLY
        3: (1,),  # INPUT
        4: (0,),  # OUTPUT
        5: (0, 0),  # JUMP-IF-TRUE
        6: (0, 0),  # JUMP-IF-FALSE
        7: (0, 0, 1),  # LESS THAN
        8: (0, 0, 1),  # EQUALS
        9: (0,),  # ADJUST RELATIVE BASE
        99: (),  # EXIT
    }

    pointer = 0
    relbase = 0
    while True:
        instruction = str(memory[pointer]).zfill(5)

        # 0: position mode
        # 1: immediate mode
        # 2: relative mode
        param_modes = tuple(map(int, instruction[:-2][::-1]))
        opcode = int(instruction[-2:])

        params = []
        for index, (param_type, mode) in enumerate(
            zip(param_types[opcode], param_modes), start=1
        ):
            if param_type == 0:  # read parameter
                if mode == 2:
                    param = memory[relbase + memory[pointer + index]]
                elif mode == 1:
                    param = memory[pointer + index]
                elif mode == 0:
                    param = memory[memory[pointer + index]]
                else:
                    raise ValueError(f"Unknown mode for read parameter: {mode}")
            elif param_type == 1:  # write parameter
                if mode == 2:
                    param = relbase + memory[pointer + index]
                elif mode == 0:
                    param = memory[pointer + index]
                else:
                    raise ValueError(
                        f"Unknown mode for write parameter: {mode}"
                    )
            else:
                raise ValueError(f"Unknown parameters type: {param_type}")

            params.append(param)

        if opcode == 1:  # ADD
            memory[params[2]] = params[0] + params[1]

            pointer += len(params) + 1
        elif opcode == 2:  # MULTIPLY
            memory[params[2]] = params[0] * params[1]

            pointer += len(params) + 1
        elif opcode == 3:  # INPUT
            try:
                value = inputqueue.get_nowait()
            except StopIteration:
                print("no enough inputs")
                return
            memory[params[0]] = value

            pointer += len(params) + 1
        elif opcode == 4:  # OUTPUT
            yield params[0]

            pointer += len(params) + 1
        elif opcode == 5:  # JUMP-IF-TRUE
            if params[0]:
                pointer = params[1]
            else:
                pointer += len(params) + 1
        elif opcode == 6:  # JUMP-IF-FALSE
            if not params[0]:
                pointer = params[1]
            else:
                pointer += len(params) + 1
        elif opcode == 7:  # LESS THAN
            if params[0] < params[1]:
                memory[params[2]] = 1
            else:
                memory[params[2]] = 0

            pointer += len(params) + 1
        elif opcode == 8:  # EQUALS
            if params[0] == params[1]:
                memory[params[2]] = 1
            else:
                memory[params[2]] = 0

            pointer += len(params) + 1
        elif opcode == 9:  # ADJUST RELATIVE BASE
            relbase += params[0]

            pointer += len(params) + 1
        elif opcode == 99:
            return
        else:
            raise ValueError(f"ERROR: unknown opcode {opcode}")


def p1(data, is_sample):
    source = list(map(int, data[0].split(",")))
    inputqueue = SimpleQueue()

    inputqueue.put_nowait(1)
    computer = intcode(source, inputqueue)

    return list(computer)

def p2(data, is_sample):
    source = list(map(int, data[0].split(",")))
    inputqueue = SimpleQueue()

    inputqueue.put_nowait(2)
    computer = intcode(source, inputqueue)

    return list(computer)
