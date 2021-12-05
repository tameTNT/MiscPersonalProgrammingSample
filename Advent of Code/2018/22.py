from collections import OrderedDict


def cave(target_x, target_y, cave_depth):
    area = OrderedDict({(X, Y): list() for X in range(target_x+1) for Y in range(target_y+1)})

    for region in area:
        if region == (0, 0):
            geologic_index = 0
        elif region == (target_x, target_y):
            geologic_index = 0
        elif region[1] == 0:
            geologic_index = region[0] * 16807
        elif region[0] == 0:
            geologic_index = region[1] * 48271
        else:
            geologic_index = area[(region[0] - 1, region[1])][0] * area[(region[0], region[1] - 1)][0]

        erosion_level = (geologic_index + cave_depth) % 20183
        area[region].append(erosion_level)

        if erosion_level % 3 == 0:
            area[region].append("rocky")
        elif erosion_level % 3 == 1:
            area[region].append("wet")
        elif erosion_level % 3 == 2:
            area[region].append("narrow")

    risk_level = 0
    print_string = str()
    for Y in range(target_y+1):
        for X in range(target_x+1):
            if area[(X, Y)][1] == "rocky":
                risk_level += 0
                print_string += "."
            elif area[(X, Y)][1] == "wet":
                risk_level += 1
                print_string += "="
            elif area[(X, Y)][1] == "narrow":
                risk_level += 2
                print_string += "|"

        print_string += "\n"

    # print(print_string)
    return risk_level


print("Part 1: ", cave(7, 701, 11394))
