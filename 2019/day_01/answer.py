def p1(data, is_sample):
    return sum((int(mass) // 3) - 2 for mass in data)


def p2(data, is_sample):
    def fuel_req(mass):
        return max((mass // 3) - 2, 0)

    fuel_req_total = 0
    for mass in map(int, data):
        fuel_req_subtotal = True
        while fuel_req_subtotal:
            fuel_req_subtotal = fuel_req(mass)
            fuel_req_total += fuel_req_subtotal
            mass = fuel_req_subtotal

    return fuel_req_total
