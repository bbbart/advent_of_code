def p1(data, is_sample):
    facing = 0  # N = 0, E = 1, S = 2, W = 3
    pos = (0, 0)
    for instruction in data[0].split(', '):
        turn = instruction[0]
        if turn == 'L':
            facing = (facing - 1) % 4
        elif turn == 'R':
            facing = (facing + 1) % 4
        else:
            raise ValueError('Unknown turn: ' + turn)

        steps = int(instruction[1:])
        if facing == 0:
            pos = (pos[0], pos[1] + steps)
        elif facing == 1:
            pos = (pos[0] + steps, pos[1])
        elif facing == 2:
            pos = (pos[0], pos[1] - steps)
        elif facing == 3:
            pos = (pos[0] - steps, pos[1])

    return abs(pos[0]) + abs(pos[1])

def p2(data, is_sample):
    facing = 0  # N = 0, E = 1, S = 2, W = 3
    pos = (0, 0)
    path = [pos]
    for instruction in data[0].split(', '):
        turn = instruction[0]
        if turn == 'L':
            facing = (facing - 1) % 4
        elif turn == 'R':
            facing = (facing + 1) % 4
        else:
            raise ValueError('Unknown turn: ' + turn)

        steps = int(instruction[1:])
        for _ in range(steps):
            if facing == 0:
                pos = (pos[0], pos[1] + 1)
            elif facing == 1:
                pos = (pos[0] + 1, pos[1])
            elif facing == 2:
                pos = (pos[0], pos[1] - 1)
            elif facing == 3:
                pos = (pos[0] - 1, pos[1])
            if pos in path:
                return abs(pos[0]) + abs(pos[1])
            path.append(pos)

    return abs(pos[0]) + abs(pos[1])
