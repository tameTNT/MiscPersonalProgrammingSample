from aocscrapper import get_AoC_input
from functools import reduce

if __name__ == '__main__':
    input_s = [x for x in get_AoC_input(2020, 13, get_test=False).strip().split('\n')]
    earliest_time = int(input_s[0])
    buses = [int(x) for x in input_s[1].split(',') if x != 'x']

    waiting_times = list()
    for bus_id in buses:
        waiting_times.append((earliest_time//bus_id + 1) * bus_id - earliest_time)

    fastest = min(waiting_times)
    earliest_id = buses[waiting_times.index(fastest)]
    print('Part 1:', fastest * earliest_id)

    # ITERATIVE SOLUTION - too slow
    # def simulate_timestep(cycle_dict, step=1):
    #     for bus_id, pos in cycle_dict.items():
    #         if bus_id != 'x':
    #             pos += step
    #             pos %= int(bus_id)
    #             cycle_dict[bus_id] = pos
    #
    #
    # order_list = input_s[1].split(',')
    # bus_dict = {bus_id: 0 for bus_id in order_list}
    # consec_index = 0
    #
    # t = 0
    # start_t = 0
    # while consec_index < len(order_list):
    #     t += 1
    #     simulate_timestep(bus_dict)
    #
    #     relevant_bus_id = order_list[consec_index]
    #     if bus_dict[relevant_bus_id] == 1:
    #         consec_index += 1
    #     elif relevant_bus_id == 'x':
    #         consec_index += 1
    #     else:
    #         consec_index = 0
    #         # required step to get first bus to 0 (back to station)
    #         required_step = int(order_list[0]) - bus_dict[order_list[0]]
    #         simulate_timestep(bus_dict, step=required_step)
    #         t += required_step
    #         start_t = t
    # print('Part 2:', start_t)  # 1202161486

    timetable = input_s[1].split(',')
    bus_index_dict = {x: timetable.index(str(x)) for x in buses}  # dict of bus_id: t-offset

    # e.g. with the buses: 3,x,x,4,5; this system of equations needs to be solved:
    # (for a time, t, that the first bus enters the station, 0)
    # t =      0       (mod    3    )  i.e. bus is at station, 0
    # t =     -3       (mod    4    )  i.e. bus is 3 steps from reaching station, 0, at time t
    # t =     -4       (mod    5    )  i.e. bus is 4 steps from reaching station, 0, at time t
    #
    # In general,
    # t = -'bus index' (mod 'bus id')
    # assuming all bus ids coprime

    # https://youtu.be/zIFehsBHB8o - Chinese Remainder Theorem by Maths with Jay
    # https://www.wikiwand.com/en/Chinese_remainder_theorem

    def find_inv(n, mod):
        # A trial and error implementation
        diff = n - mod * (n // mod)  # distance from (LCM of mod) < n
        x = 1
        while (diff * x) % mod != 1:  # inverse defined as equaling 1
            x += 1
        return x

    result = 0
    N = reduce(lambda x, y: x*y, buses)  # finds product of moduli (the 'bus id's)
    for bus_id in buses:  # for each modulus value
        remainder = -bus_index_dict[bus_id]  # bi: needs to be -ve because buses arrive *before* time, t
        Ni = N // bus_id  # moduli product DIV modulus
        result += remainder * Ni * find_inv(Ni, bus_id)

    print('Part 2:', result % N)

    # from sympy.ntheory.modular import crt
    # crt_sol = crt(m=buses, v=bus_index_dict.values())  # moduli, remainders
    # print('Part 2:', crt_sol[1] % crt_sol[0])
