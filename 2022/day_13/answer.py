from dataclasses import dataclass
from itertools import zip_longest


@dataclass
class Packet:
    data: list

    def __lt__(self, other):
        for left, right in zip_longest(self.data, other.data, fillvalue=-1):
            left_type = type(left)
            right_type = type(right)

            # both are ints
            if left_type == int and right_type == int:
                if left == right:
                    continue
                return left < right

            # at least one of them is a list, so let's ensure they both are
            if left_type == int:
                left = [left]
            if right_type == int:
                right = [right]

            # both are lists
            if left == right:
                continue
            return Packet(left) < Packet(right)

        return False


# pylint: disable=eval-used
# It's actually pretty useful here, given we check the input :-)
def p1(data):
    packet_pairs = []
    packet_left, packet_right = None, None
    for line in data:
        if line == "":
            packet_left, packet_right = None, None
            continue
        if not packet_left:
            packet_left = Packet(eval(line))
        else:
            packet_right = Packet(eval(line))
            packet_pairs.append((packet_left, packet_right))

    index_right_order = []
    for index, pair in enumerate(packet_pairs, start=1):
        if pair[0] < pair[1]:
            index_right_order.append(index)

    return sum(index_right_order)


# pylint: disable=eval-used
# It's actually pretty useful here, given we check the input :-)
def p2(data):
    divider_2 = Packet([[2]])
    divider_6 = Packet([[6]])
    packets = [divider_2, divider_6]
    for line in data:
        if line == "":
            continue
        packets.append(Packet(eval(line)))

    ordered_packets = sorted(packets)
    return (ordered_packets.index(divider_2) + 1) * (
        ordered_packets.index(divider_6) + 1
    )
