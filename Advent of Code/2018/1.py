from itertools import cycle


def run_code():
    with open("Inputs\\Day1.txt", "r") as input_set:
        frequency = sum([int(line.strip("+")) for line in input_set])

        print("Part 1: ", frequency)

        input_set.seek(0)
        frequency = 0
        cyclical_input = cycle([int(line.strip()) for line in input_set])
        frequency_list = []

        for change in cyclical_input:
            frequency += change

            if frequency in frequency_list:
                break

            else:
                frequency_list.append(frequency)

        print("Part 2: ", frequency)


run_code()
