#!/usr/bin/env python

from dataclasses import dataclass
from itertools import chain


def p1(data: list[str], is_sample: bool):
    disk = []
    for line in data:
        for bid, char in enumerate(line):
            if bid % 2:  # odd = free space
                disk.extend([None] * int(char))
            else:
                disk.extend([bid // 2] * int(char))

    while None in disk:
        if block := disk.pop():
            disk[disk.index(None)] = block

    return sum(pos * bid for pos, bid in enumerate(disk))


def p2(data: list[str], is_sample: bool):
    # FIRST TRY (fails, answer is too low)
    # disk = []
    # max_space = 0
    # for line in data:
    #     for bid, char in enumerate(line):
    #         if char == "0":
    #             continue
    #         if bid % 2:  # odd = free space
    #             space = int(char)
    #             disk.append(space)
    #             max_space = max(max_space, space)
    #         else:
    #             disk.append([bid // 2] * int(char))

    # for block in reversed(disk.copy()):
    #     if not isinstance(block, list):
    #         continue
    #     need_space = len(block)
    #     block_i = disk.index(block)
    #     space_i = block_i
    #     for space in range(need_space, max_space + 1):
    #         try:
    #             space_i = min(space_i, disk.index(space))
    #         except ValueError:
    #             continue

    #     if space_i == block_i:
    #         continue

    #     # replace the block with empty space
    #     disk[block_i] = len(block)

    #     # insert the block and remove empty space
    #     space = disk[space_i]
    #     disk[space_i] = block
    #     if space > need_space:
    #         disk.insert(space_i + 1, space - need_space)

    #     # merge empty space
    #     accumulator = 0
    #     to_remove = []
    #     for item_i, item in reversed(list(enumerate(disk))):
    #         if isinstance(item, int):
    #             accumulator += item
    #             to_remove.append(item_i)
    #         else:
    #             if accumulator == 0:
    #                 continue
    #             disk[item_i + 1] = accumulator
    #             for _ in range(len(to_remove) - 1):
    #                 disk.pop(to_remove[1])
    #             accumulator = 0
    #             to_remove = []

    # return sum(
    #     pos * bid
    #     for pos, bid in enumerate(
    #         chain.from_iterable(
    #             [0]*item if isinstance(item, int) else item for item in disk
    #         )
    #     )
    # )

    # SECOND TRY (fails, answer is too low)
    # @dataclass
    # class Block:
    #     size: int
    #     bid: int
    #     __current: int = 0

    #     def __repr__(self):
    #         return self.size * str(self.bid)

    #     def __iter__(self):
    #         return self

    #     def __next__(self):
    #         if self.__current < self.size:
    #             self.__current += 1
    #             return self.bid
    #         raise StopIteration


    # class Empty:
    #     def __init__(self, size: int):
    #         self.size = size
    #         self.__current = 0

    #     def decrease(self, delta: int):
    #         self.size -= delta

    #     def increase(self, delta: int):
    #         self.size += delta

    #     def fits(self, block: Block):
    #         return self.size >= block.size

    #     def __repr__(self):
    #         return "." * self.size

    #     def __iter__(self):
    #         return self

    #     def __next__(self):
    #         if self.__current < self.size:
    #             self.__current += 1
    #             return 0
    #         raise StopIteration

    # disk = []
    # for bid, char in enumerate(data[0]):
    #     if bid % 2:
    #         disk.append(Empty(int(char)))
    #     else:
    #         disk.append(Block(int(char), bid // 2))

    # for block in reversed(disk.copy()):
    #     if not isinstance(block, Block):
    #         continue
    #     block_i = disk.index(block)
    #     for addr, empty in enumerate(disk):
    #         if block_i < addr:  # we only want to move blocks forward
    #             break
    #         if not isinstance(empty, Empty):
    #             continue
    #         if empty.fits(block):
    #             before, after = None, None
    #             if block_i > 0:
    #                 before = disk[block_i - 1]
    #             if block_i < len(disk) - 1:
    #                 after = disk[block_i + 1]

    #             # replace the block with empty space
    #             new_empty =  Empty(block.size)
    #             disk[block_i] = new_empty

    #             # merge with possible empty space before
    #             if isinstance(before, Empty):
    #                 new_empty.increase(before.size)
    #                 disk.remove(before)
    #             # merge with possible empty space after
    #             if isinstance(after, Empty):
    #                 new_empty.increase(after.size)
    #                 disk.remove(after)

    #             # disk[disk.index(block)] = Empty(block.size)
    #             disk[addr] = block
    #             empty.decrease(block.size)
    #             if empty.size:
    #                 disk.insert(addr + 1, empty)
    #             break

    # return sum(pos * bid for pos, bid in enumerate(chain.from_iterable(disk)))
    
    return 'N/A'
