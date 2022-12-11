def is_visible(x, y, forest):
    grid_size = len(forest)

    # trees on the edge are always visible
    if x in (0, grid_size - 1) or y in (0, grid_size - 1):
        return True

    this_tree = forest[x][y]

    visible_from_left = all(
        forest[x][other_y] < this_tree for other_y in range(y)
    )
    visible_from_right = all(
        forest[x][other_y] < this_tree for other_y in range(y + 1, grid_size)
    )
    visible_from_top = all(
        forest[other_x][y] < this_tree for other_x in range(x)
    )
    visible_from_bottom = all(
        forest[other_x][y] < this_tree for other_x in range(x + 1, grid_size)
    )
    return any(
        (
            visible_from_left,
            visible_from_right,
            visible_from_top,
            visible_from_bottom,
        )
    )


def scenic_score(x, y, forest):
    grid_size = len(forest)

    # trees on the edge have at least one vieweing distance of zero
    if x in (0, grid_size - 1) or y in (0, grid_size - 1):
        return 0

    this_tree = forest[x][y]

    scenic_score_left = 0
    for other_y in range(y - 1, -1, -1):
        scenic_score_left += 1
        if forest[x][other_y] >= this_tree:
            break

    scenic_score_right = 0
    for other_y in range(y + 1, grid_size):
        scenic_score_right += 1
        if forest[x][other_y] >= this_tree:
            break

    scenic_score_up = 0
    for other_x in range(x - 1, -1, -1):
        scenic_score_up += 1
        if forest[other_x][y] >= this_tree:
            break

    scenic_score_down = 0
    for other_x in range(x + 1, grid_size):
        scenic_score_down += 1
        if forest[other_x][y] >= this_tree:
            break

    return (
        scenic_score_left
        * scenic_score_right
        * scenic_score_up
        * scenic_score_down
    )


def p1(data):
    forest = []
    for line in data:
        forest.append(list(line))

    grid_size = len(forest)
    return sum(
        1 if is_visible(x, y, forest) else 0
        for x in range(grid_size)
        for y in range(grid_size)
    )


def p2(data):
    forest = []
    for line in data:
        forest.append(list(line))

    grid_size = len(forest)
    return max(
        scenic_score(x, y, forest)
        for x in range(grid_size)
        for y in range(grid_size)
    )
