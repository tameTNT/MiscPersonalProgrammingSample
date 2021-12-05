import operator


def taxicab_distance(coords1, coords2):
    return abs(coords2[0] - coords1[0]) + abs(coords2[1] - coords1[1]) + abs(coords2[2] - coords1[2])


with open("Inputs\\Day23.txt", "r") as input_set:
    nanobots = [line.strip() for line in input_set]
    nanobots = {i: nanobots[i].split(", ") for i in range(len(nanobots))}

    for nanobot_number in nanobots:
        nanobots[nanobot_number][0], nanobots[nanobot_number][1] = int(nanobots[nanobot_number][1].strip("r=")), [int(x) for x in nanobots[nanobot_number][0].strip("pos=<>").split(",")]

    strongest_nanobot = max(nanobots.items(), key=operator.itemgetter(1))[0]
    strongest_range = nanobots[strongest_nanobot][0]
    strongest_pos = nanobots[strongest_nanobot][1]
    nanobots_in_range = 0

    for nanobot_number in nanobots:
        nanobot_pos = nanobots[nanobot_number][1]
        if taxicab_distance(nanobot_pos, strongest_pos) <= strongest_range:
            nanobots_in_range += 1

    print("Part 1: ", nanobots_in_range)
    x_range = [nanobot[1][0] for nanobot in nanobots.values()]
    y_range = [nanobot[1][1] for nanobot in nanobots.values()]
    z_range = [nanobot[1][2] for nanobot in nanobots.values()]
    largest_x = max(x_range)
    largest_y = max(y_range)
    largest_z = max(z_range)
    smallest_x = min(x_range)
    smallest_y = min(y_range)
    smallest_z = min(z_range)

    points = dict()
    for Z in range(smallest_z, largest_z+1):
        for Y in range(smallest_y, largest_y+1):
            for X in range(smallest_x, largest_x+1):
                nanobots_in_range = 0
                for nanobot in nanobots:
                    if taxicab_distance(nanobots[nanobot][1], (X, Y, Z)) <= nanobots[nanobot][0]:
                        nanobots_in_range += 1
                points[(X, Y, Z)] = nanobots_in_range

    print("Part 2: ", taxicab_distance(max(points.items(), key=operator.itemgetter(1))[0], (0, 0, 0)))
