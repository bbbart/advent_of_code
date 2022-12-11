def find_marker(line, blocklen):
    for index in range(len(line) - blocklen):
        block = set(line[index : index + blocklen])
        if len(block) == blocklen:
            return index + blocklen
    return 0


def p1(data):
    blocklen = 4
    markers = []
    for line in data:
        markers.append(find_marker(line, blocklen))
    return ", ".join(map(str, markers))


def p2(data):
    blocklen = 14
    markers = []
    for line in data:
        markers.append(find_marker(line, blocklen))
    return ", ".join(map(str, markers))
