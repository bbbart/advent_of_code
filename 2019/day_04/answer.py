def is_valid_password_p1(number):
    numberstr = str(number)

    # six-digit number (guaranteed by input range)
    # if len(numberstr) != 6:
    #     return False

    # digits never decrease
    if (
        numberstr[0] > numberstr[1]
        or numberstr[1] > numberstr[2]
        or numberstr[2] > numberstr[3]
        or numberstr[3] > numberstr[4]
        or numberstr[4] > numberstr[5]
    ):
        return False

    # two adjacent digits are the same
    if (
        numberstr[0] != numberstr[1]
        and numberstr[1] != numberstr[2]
        and numberstr[2] != numberstr[3]
        and numberstr[3] != numberstr[4]
        and numberstr[4] != numberstr[5]
    ):
        return False

    return True


def is_valid_password_p2(number):
    if not is_valid_password_p1(number):
        return False

    numberstr = str(number)

    # the two adjacent matching digits are not part of a larger group of
    # matching digits
    if 2 not in (numberstr.count(f"{i}") for i in range(10)):
        return False

    return True


def p1(data, is_sample):
    range_min, range_max = map(int, data[0].split("-"))

    return sum(
        is_valid_password_p1(number)
        for number in range(range_min + 1, range_max)
    )


def p2(data, is_sample):
    range_min, range_max = map(int, data[0].split("-"))

    return sum(
        is_valid_password_p2(number)
        for number in range(range_min + 1, range_max)
    )
