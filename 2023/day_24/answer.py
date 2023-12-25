#!/usr/bin/env python

from itertools import combinations

from sympy import Point, Polygon, Ray


def p1(data, is_sample):
    # this works, but takes almost eight minutes to complete on my machine
    return "done"
    if not is_sample:
        mini = 200_000_000_000_000
        maxi = 400_000_000_000_000
    else:
        mini = 7
        maxi = 27
    rect = Polygon(
        Point(mini, mini),
        Point(mini, maxi),
        Point(maxi, maxi),
        Point(maxi, mini),
    )

    hailstone_trajectories = set()
    for line in data:
        p, v = line.split("@")
        px, py, _ = tuple(map(int, p.split(",")))
        vx, vy, _ = tuple(map(int, v.split(",")))
        hailstone_trajectories.add(Ray(Point(px, py), Point(px + vx, py + vy)))

    intersect_counter = 0
    for t1, t2 in combinations(hailstone_trajectories, 2):
        for ip in t1.intersection(t2):
            if rect.encloses_point(ip) or rect.contains(ip):
                intersect_counter += 1
                break

    return intersect_counter


def p2(data, is_sample):
    if not is_sample:
        return "N/A"
    return "N/A"

    # didn't have time to start working on this one;
    #
    # first thoughts: we have to solve for px, py, pz, vx, vy and vz such that,
    # for every given 'ray' there exists a t for which both equations are
    # equal. I actually reckon that working with six is enough to get to a
    # solution. The sample input only has five, so either that solution is not
    # unique, or it is made unique by the additional requirement that we can
    # only start at positions with integer coordinates and move at velocities
    # with integer cooridinates.
