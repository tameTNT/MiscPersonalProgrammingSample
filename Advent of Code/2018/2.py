from collections import Counter
from difflib import ndiff


def run_code():
    with open("Inputs\\Day2.txt", "r") as input_set:
        two_count = 0
        three_count = 0
        for line in input_set:
            letter_frequencies = Counter(line)
            if 2 in letter_frequencies.values():
                two_count += 1
            if 3 in letter_frequencies.values():
                three_count += 1

        print("Part 1: ", two_count * three_count)

        input_set.seek(0)
        id_list = [line.strip() for line in input_set]
        input_set.seek(0)
        for line in input_set:
            for ID in id_list:
                plus_count = 0
                minus_count = 0
                difference_list = list(ndiff(line.strip(), ID))
                for character in difference_list:
                    if "+" in character:
                        plus_count += 1
                    if "-" in character:
                        minus_count += 1

                if plus_count == 1 and minus_count == 1:
                    same_list = [comparison[-1] for comparison in difference_list if comparison[0] == " "]
                    print("Part 2: {}".format("".join(same_list)))
                    return


run_code()
