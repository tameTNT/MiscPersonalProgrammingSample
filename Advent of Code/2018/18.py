from collections import Counter


def woodland(minutes):
    def check(location_check, check_type):
        try:
            if location_check >= 0:
                if check_type == "tree":
                    if stringed_landscape[location_check] == "|":
                        return True
                    else:
                        return False
                elif check_type == "lumberyard":
                    if stringed_landscape[location_check] == "#":
                        return True
                    else:
                        return False
            else:
                return False
        except IndexError:
            return False

    with open("Inputs\\Day18.txt", "r") as input_set:
        width = len(input_set.read().split("\n")[0])
        input_set.seek(0)
        stringed_landscape = "".join([line.strip() for line in input_set])
        past_landscapes = list()
        loop_start_minute = int()
        loop_has_started = False
        loop = list()

        for minute in range(1, minutes+1):  # 1 start and '+1ed' end needed for part 2

            # PART 2 relies on this if/else bracket below
            if stringed_landscape in past_landscapes or loop_has_started:  # Checks if the landscape has happened before or if the loop has already started
                if not loop_has_started:  # This branch is only entered once and just sets the minute at which it starts
                    loop_start_minute = minute
                    loop_has_started = True
                else:
                    if stringed_landscape in loop:  # Once the end of the loop has been found (the landscape begins to repeat itself) this branch is entered
                        counts = Counter(loop[(minutes - loop_start_minute) % len(loop)])  # Finds the index in the loop of the 'minutes' iteration of the landscape using modulo and then finds the count as normal
                        score = counts["|"] * counts["#"]
                        return score
                    else:
                        loop.append(stringed_landscape)
            else:
                past_landscapes.append(stringed_landscape)  # Keeps a record of the landscape after every minute

            next_minute = str()

            for acre in range(len(stringed_landscape)):

                line_place = acre % width

                if stringed_landscape[acre] == ".":
                    count = 0
                    if check(acre - 1, "tree") and line_place != 0:
                        count += 1
                    if check(acre + 1, "tree") and line_place != width-1:
                        count += 1
                    if check(acre - width - 1, "tree") and line_place != 0:
                        count += 1
                    if check(acre - width, "tree"):
                        count += 1
                    if check(acre - width + 1, "tree") and line_place != width-1:
                        count += 1
                    if check(acre + width - 1, "tree") and line_place != 0:
                        count += 1
                    if check(acre + width, "tree"):
                        count += 1
                    if check(acre + width + 1, "tree") and line_place != width-1:
                        count += 1

                    if count >= 3:
                        next_minute += "|"
                    else:
                        next_minute += "."

                elif stringed_landscape[acre] == "|":
                    count = 0

                    if check(acre - 1, "lumberyard") and line_place != 0:
                        count += 1
                    if check(acre + 1, "lumberyard") and line_place != width-1:
                        count += 1
                    if check(acre - width - 1, "lumberyard") and line_place != 0:
                        count += 1
                    if check(acre - width, "lumberyard"):
                        count += 1
                    if check(acre - width + 1, "lumberyard") and line_place != width-1:
                        count += 1
                    if check(acre + width - 1, "lumberyard") and line_place != 0:
                        count += 1
                    if check(acre + width, "lumberyard"):
                        count += 1
                    if check(acre + width + 1, "lumberyard") and line_place != width-1:
                        count += 1

                    if count >= 3:
                        next_minute += "#"
                    else:
                        next_minute += "|"

                elif stringed_landscape[acre] == "#":
                    lumberyard_count = 0
                    tree_count = 0

                    if check(acre - 1, "lumberyard") and line_place != 0:
                        lumberyard_count += 1
                    if check(acre + 1, "lumberyard") and line_place != width-1:
                        lumberyard_count += 1
                    if check(acre - width - 1, "lumberyard") and line_place != 0:
                        lumberyard_count += 1
                    if check(acre - width, "lumberyard"):
                        lumberyard_count += 1
                    if check(acre - width + 1, "lumberyard") and line_place != width-1:
                        lumberyard_count += 1
                    if check(acre + width - 1, "lumberyard") and line_place != 0:
                        lumberyard_count += 1
                    if check(acre + width, "lumberyard"):
                        lumberyard_count += 1
                    if check(acre + width + 1, "lumberyard") and line_place != width-1:
                        lumberyard_count += 1

                    if check(acre - 1, "tree") and line_place != 0:
                        tree_count += 1
                    if check(acre + 1, "tree") and line_place != width-1:
                        tree_count += 1
                    if check(acre - width - 1, "tree") and line_place != 0:
                        tree_count += 1
                    if check(acre - width, "tree"):
                        tree_count += 1
                    if check(acre - width + 1, "tree") and line_place != width-1:
                        tree_count += 1
                    if check(acre + width - 1, "tree") and line_place != 0:
                        tree_count += 1
                    if check(acre + width, "tree"):
                        tree_count += 1
                    if check(acre + width + 1, "tree") and line_place != width-1:
                        tree_count += 1

                    if lumberyard_count >= 1 and tree_count >= 1:
                        next_minute += "#"
                    else:
                        next_minute += "."

            stringed_landscape = next_minute

        counts = Counter(stringed_landscape)
        score = counts["|"] * counts["#"]
        return score


print("Part 1: ", woodland(10))
print("Part 2: ", woodland(1000000000))
