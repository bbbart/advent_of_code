#!/usr/bin/env python

from collections import namedtuple

Race = namedtuple("Race", ("time", "record"))


def race_distance(race, button_time):
    speed = button_time
    time = race.time - button_time
    return time * speed


def p1(data, is_sample):
    for line in data:
        if line.startswith("Time:"):
            times = map(int, line.split(":")[1].split())
        elif line.startswith("Distance:"):
            distances = map(int, line.split(":")[1].split())
        else:
            print("Unknown line in data found")

    races = [Race(time, record) for time, record in zip(times, distances)]

    win_options = 1
    for race in races:
        # very naive; see p2 for optimization
        win_options *= sum(
            race_distance(race, button_time) > race.record
            for button_time in range(1, race.record)
        )

    return win_options


def p2(data, is_sample):
    for line in data:
        if line.startswith("Time:"):
            time = int(line.split(":")[1].replace(" ", ""))
        elif line.startswith("Distance:"):
            distance = int(line.split(":")[1].replace(" ", ""))
        else:
            print("Unknown line in data found")
    race = Race(time, distance)

    button_time = 0
    while race_distance(race, button_time) <= race.record:
        button_time += 1

    return race.time - 2 * button_time + (1 if race.time // 2 else 0)
