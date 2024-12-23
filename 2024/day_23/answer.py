#!/usr/bin/env python

from collections import defaultdict


def p1(data: list[str], is_sample: bool):
    network: dict[str, set[str]] = defaultdict(list)
    for line in data:
        computers = line.split("-")
        network[computers[0]].append(computers[1])
        network[computers[1]].append(computers[0])

    triangles: list[set[str]] = []
    for computer in network:
        if not computer.startswith("t"):
            continue
        for neighbour in network[computer]:
            for common in set(network[computer]) & set(network[neighbour]):
                triangle = set((computer, neighbour, common))
                if triangle not in triangles:
                    triangles.append(triangle)

    return len(triangles)


def p2(data: list[str], is_sample: bool):
    network: dict[str, set[str]] = defaultdict(set)
    for line in data:
        computers = line.split("-")
        network[computers[0]].add(computers[1])
        network[computers[1]].add(computers[0])

    def bron_kerbosch(graph, R, P, X, cliques):
        if not P and not X:
            cliques.append(R)
            return
        for node in P.copy():
            bron_kerbosch(
                graph,
                R | {node},  # Add node to the current clique
                P & set(graph[node]),  # Potential candidates
                X & set(graph[node]),  # Exclude already visited nodes
                cliques,
            )
            P.remove(node)
            X.add(node)

    def find_largest_clique(graph):
        cliques = []
        bron_kerbosch(graph, set(), set(graph.keys()), set(), cliques)
        return max(cliques, key=len)

    largest_clique = find_largest_clique(network)
    return ','.join(sorted(largest_clique))
