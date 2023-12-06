#!/usr/bin/env python

import re
from collections import deque
from dataclasses import dataclass
from functools import reduce

MAP_PARSE = re.compile(r"(?P<src>.+)-to-(?P<dst>.+) map:")


@dataclass
class Map:
    dst: str
    src: str
    dst_range_starts: list[int]
    src_range_starts: list[int]
    range_lengths: list[int]

    def map(self, src_int: int) -> int:
        for dst_range_start, src_range_start, range_length in zip(
            self.dst_range_starts, self.src_range_starts, self.range_lengths
        ):
            if (
                src_int < src_range_start
                or src_int > src_range_start + range_length
            ):
                continue
            return src_int - src_range_start + dst_range_start

        return src_int


def p1(data, is_sample):
    # parse the almanac
    seeds = map(int, data[0].split(":")[1].split())
    maps: dict[str, Map] = {}
    for line in data[2:]:
        if not line:
            continue

        map_title = MAP_PARSE.match(line)
        if map_title:
            dst = map_title.group("dst")
            src = map_title.group("src")
            current_map = Map(dst, src, [], [], [])
            maps[dst] = current_map
            continue

        dst_range_start, src_range_start, range_length = map(int, line.split())
        current_map.dst_range_starts.append(dst_range_start)
        current_map.src_range_starts.append(src_range_start)
        current_map.range_lengths.append(range_length)

    # trace the map route from location to seed
    map_route: list[Map] = [maps["location"]]
    src = maps["location"].src
    while src != "seed":
        map_route.append(maps[src])
        src = maps[src].src

    # calculate the lowest location number
    return min(
        reduce(lambda v, m: m.map(v), reversed(map_route), seed)
        for seed in seeds
    )


def p2(data, is_sample):
    # parse the almanac
    seed_desc = deque(map(int, data[0].split(":")[1].split()))
    seed_ranges = []
    while seed_desc:
        from_ = seed_desc.popleft()
        count = seed_desc.popleft()
        seed_ranges.append(range(from_, from_ + count))
    maps: dict[str, Map] = {}
    for line in data[2:]:
        if not line:
            continue

        map_title = MAP_PARSE.match(line)
        if map_title:
            dst = map_title.group("dst")
            src = map_title.group("src")
            current_map = Map(dst, src, [], [], [])
            maps[dst] = current_map
            continue

        dst_range_start, src_range_start, range_length = map(int, line.split())
        current_map.dst_range_starts.append(dst_range_start)
        current_map.src_range_starts.append(src_range_start)
        current_map.range_lengths.append(range_length)

    # trace the map route from location to seed
    map_route: list[Map] = [maps["location"]]
    src = maps["location"].src
    while src != "seed":
        map_route.append(maps[src])
        src = maps[src].src

    # calculate the lowest location number
    # works, but takes a couple of hours... :-)
    # very limited memory use however!
    return min(
        reduce(lambda v, m: m.map(v), reversed(map_route), seed)
        for seeds in seed_ranges
        for seed in seeds
    )
