from collections import defaultdict, deque


def data_to_graph(data):
    # an adjacency list for representing the graph
    graph = defaultdict(list)
    for line in data:
        centre, orbiter = line.split(")")
        graph[centre].append(orbiter)

    return graph


def p1(data, is_sample):
    graph = data_to_graph(data)

    # calculate the distances to the root for each vertex
    distances = defaultdict(int)
    distances["COM"] = 0

    visited = set()

    # BFS queue
    queue = deque(["COM"])

    while queue:
        current = queue.popleft()
        visited.add(current)

        for neighbour in graph[current]:
            if neighbour not in visited:
                distances[neighbour] = distances[current] + 1
                queue.append(neighbour)
                visited.add(neighbour)

    return sum(distances.values())


def p2(data, is_sample):
    graph = data_to_graph(data)

    if is_sample:
        graph["K"].append("YOU")
        graph["I"].append("SAN")

    # build parent map
    parent_map = {}
    queue = [("COM", None)]

    while queue:
        current, parent = queue.pop(0)
        parent_map[current] = parent
        for neighbour in graph[current]:
            queue.append((neighbour, current))

    # find ancestors
    ancestors_you = []
    current = "YOU"
    while current is not None:
        ancestors_you.append(current)
        current = parent_map.get(current)

    ancestors_san = []
    current = "SAN"
    while current is not None:
        ancestors_san.append(current)
        current = parent_map.get(current)

    # find LCA (lowest common ancestor)
    lca = "COM"
    for ancestor in ancestors_san:
        if ancestor in ancestors_you:
            lca = ancestor
            break

    distance1 = ancestors_you.index(lca) - 1
    distance2 = ancestors_san.index(lca) - 1

    return distance1 + distance2
