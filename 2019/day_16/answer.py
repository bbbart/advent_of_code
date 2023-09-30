from itertools import cycle


def p1(data, is_sample):
    elements = list(map(int, data[0]))

    def pattern_for_index(index: int):
        base_pattern = cycle((0, 1, 0, -1))

        def pattern():
            while True:
                pattern_digit = next(base_pattern)
                for _ in range(index):
                    yield pattern_digit

        p = pattern()
        next(p)
        return p

    phase = 0
    while phase < 100:
        new_elements = []
        for i in range(len(elements)):
            new_elements.append(
                abs(
                    sum(
                        p * d
                        for p, d in zip(elements, pattern_for_index(1 + i))
                    )
                )
                % 10
            )
        elements = new_elements
        phase += 1

    return "".join(map(str, elements[:8]))


def p2(data, is_sample):
    return 'N/A'
    # I think I got pretty far here with an optimised summing-algorithm, that
    # kept in mind the repetitive nature of both the pattern and the input, but
    # it was still waaaaaay too slow.
    #
    # After reading
    # https://www.reddit.com/r/adventofcode/comments/rtbx8x/2019_day_16_part_2_a_story_a_solution/,I
    # don't think i deserve the star - even though I do understand the
    # explanation. :-)
    #
    # I don't think I would have come up with the idea to only look at the
    # second half of the element list by myself.
