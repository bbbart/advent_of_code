#!/usr/bin/env python


def p1(data: list[str], is_sample: bool):
    stones = map(int, data[0].split())

    for _ in range(25):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif not (length := len(str(stone))) % 2:
                new_stones.append(int(str(stone)[:length//2]))
                new_stones.append(int(str(stone)[length//2:]))
            else:
                new_stones.append(2024 * stone)
        stones = new_stones
        print(len(stones))

    return len(stones)


def p2(data: list[str], is_sample: bool):
    if is_sample:
        return "N/A"
    return "N/A"

    # this method is too naive and runs out of memory
    # I guess the idea is to find repetitive loops and determine the resulting
    # length without simply calculating it.
    # for example:
    # 0 -> 1 -> 2024 -> 20 24 -> 2 0 2 4 -> and there is another 0
    # stones = map(int, data[0].split())

    # for _ in range(75):
    #     new_stones = []
    #     for stone in stones:
    #         if stone == 0:
    #             new_stones.append(1)
    #         elif not (length := len(str(stone))) % 2:
    #             new_stones.append(int(str(stone)[:length//2]))
    #             new_stones.append(int(str(stone)[length//2:]))
    #         else:
    #             new_stones.append(2024 * stone)
    #     stones = new_stones

    # return len(stones)
