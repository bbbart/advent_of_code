from collections import defaultdict
from dataclasses import dataclass


@dataclass
class SNAFU:
    elf: str

    # pylint: disable=too-many-branches
    # It's base 5
    def __add__(self, other):
        result_breakdown = defaultdict(int)
        for index in range(max(*self.breakdown, *other.breakdown) + 1):
            result_breakdown[index] = (
                self.breakdown[index] + other.breakdown[index]
            )

        result = ""
        for index in range(max(result_breakdown) + 1):
            digit = result_breakdown[index]
            if digit == 5:
                result += "0"
                result_breakdown[index + 1] += 1
            elif digit == 4:
                result += "-"
                result_breakdown[index + 1] += 1
            elif digit == 3:
                result += "="
                result_breakdown[index + 1] += 1
            elif digit == 2:
                result += "2"
            elif digit == 1:
                result += "1"
            elif digit == 0:
                result += "0"
            elif digit == -1:
                result += "-"
            elif digit == -2:
                result += "="
            elif digit == -3:
                result += "2"
                result_breakdown[index + 1] -= 1
            elif digit == -4:
                result += "1"
                result_breakdown[index + 1] -= 1
            elif digit == -5:
                result += "0"
                result_breakdown[index + 1] -= 1
        if result_breakdown[index + 1]:
            # this can only even be 1 or -1 (last carry-over)
            result += "1" if result_breakdown[index + 1] == 1 else "-"

        result = SNAFU(result[::-1])
        return result

    def __post_init__(self):
        dec = 0
        breakdown = defaultdict(int)
        for index, char in enumerate(reversed(self.elf)):
            base = 5**index
            try:
                amount = int(char)
            except ValueError:
                if char == "-":
                    amount = -1
                elif char == "=":
                    amount = -2
            dec += amount * base
            breakdown[index] = amount

        self.dec: int = dec
        self.breakdown: dict[int, int] = breakdown


def p1(data, is_sample):
    result = SNAFU("0")
    numbers = []
    for number_elf in data:
        numbers.append(SNAFU(number_elf).dec)
        result += SNAFU(number_elf)
        assert result.dec == sum(numbers)

    return result.elf
