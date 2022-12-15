from copy import deepcopy


def trav_dict(dct, kys):
    if not kys:
        return dct
    return trav_dict(dct.get(kys.pop(0)), kys)


def subdir_size(subdir):
    size = 0
    for value in subdir.values():
        if isinstance(value, dict):
            size += subdir_size(value)
        else:
            size += value
    return size


# pylint: disable=too-many-locals, too-many-branches
# This is no beauty contest.
def parse_data(data):
    # keys are either files or directories
    #   for files, values are file sizes
    #   for directors, values are dicts with the same structure
    fs = {"/": {}}
    pwd = []
    mode = None

    # parse into filesystem
    for line in data:
        if line.startswith("$"):
            line = line.lstrip("$ ")
            try:
                command, arguments = line.split(" ", 1)
            except ValueError:
                command = line
                arguments = None

            if command == "cd":
                mode = "traversing"
                if arguments == "..":
                    pwd.pop()
                else:
                    pwd.append(arguments)
            elif command == "ls":
                mode = "listing"
        else:
            if mode == "listing":
                if line.startswith("dir"):
                    dirname = line.split(" ", 1)[1]
                    trav_dict(fs, deepcopy(pwd))[dirname] = {}
                else:
                    filesize, filename = line.split(" ", 1)
                    trav_dict(fs, deepcopy(pwd))[filename] = int(filesize)

    # traverse filesystem
    to_do = [
        ["/"],
    ]
    dirsizes = {}
    for fspos in to_do:
        subdir = trav_dict(fs, deepcopy(fspos))
        for item, value in subdir.items():
            if isinstance(value, dict):
                # pylint: disable=modified-iterating-list
                # I know, this is on purpose
                to_do.append(fspos + [item])
        dirsizes["/".join(fspos)] = subdir_size(subdir)

    return dirsizes


def p1(data, is_sample):
    dirsizes = parse_data(data)

    answer = 0
    for size in dirsizes.values():
        if size > 100000:
            continue
        answer += size
    return answer


def p2(data, is_sample):
    dirsizes = parse_data(data)

    total_space = 70000000
    needed_space = 30000000
    used_space = dirsizes["/"]
    free_space = total_space - used_space
    todelete_space = needed_space - free_space

    return min(usage for usage in dirsizes.values() if usage > todelete_space)
