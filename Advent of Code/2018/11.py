from collections import OrderedDict
import operator


def largest_total_power_square(grid_serial_number, part):
    power_grid = OrderedDict({(X, Y): int() for X in range(1, 301) for Y in range(1, 301)})

    for cell in power_grid:
        rack_id = cell[0] + 10
        power_level = rack_id * cell[1]
        power_level += grid_serial_number
        power_level *= rack_id
        try:
            power_level = int(str(power_level)[-3])
        except IndexError:
            power_level = 0
        power_level -= 5

        power_grid[cell] = power_level

    if part == 1:
        square_powers = dict()
        for Y in range(1, 298):
            for X in range(1, 298):
                total_power = sum(power_grid[(X+x_add, Y+y_add)] for x_add in range(3) for y_add in range(3))  # power_grid[(X, Y)] + power_grid[(X+1, Y)] + power_grid[(X+2, Y)] + power_grid[(X, Y+1)] + power_grid[(X+1, Y+1)] + power_grid[(X+2, Y+1)] + power_grid[(X, Y+2)] + power_grid[(X+1, Y+2)] + power_grid[(X+2, Y+2)]
                square_powers[(X, Y)] = total_power

        return max(square_powers.items(), key=operator.itemgetter(1))

    elif part == 2:
        best = {"X": int(), "Y": int(), "size": int(), "power": int()}
        for size in range(1, 301):
            for Y in range(size+1, 301):
                for X in range(size+1, 301):
                    total = power_grid[(X, Y)] + power_grid[(X, Y-size)] + power_grid[(X-size, Y)] - power_grid[(X-size, Y-size)]  # https://en.wikipedia.org/wiki/Summed-area_table
                    if total > best["power"]:
                        best["X"] = X
                        best["Y"] = Y
                        best["size"] = size
                        best["power"] = total

        return best["X"], best["Y"], best["size"]


print("Part 1: ", largest_total_power_square(9435, 1)[0])
print("Part 2: ", largest_total_power_square(18, 2))
