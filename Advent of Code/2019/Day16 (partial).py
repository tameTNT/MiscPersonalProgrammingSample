from aocscrapper import get_AoC_input
from operator import mul

days_input = "03036732577212944063491565474664"  # get_AoC_input(2019, 16).strip()
split_input = [int(x) for x in list(str(days_input))]


def return_repeating_pattern(base_pattern, position, num_digits):
    length_of_pattern = len(base_pattern)
    position_considered = list()
    for i in range(length_of_pattern):
        position_considered += [base_pattern[i]] * position
    sequence_repeats_needed = (num_digits // (length_of_pattern*position)) + 1
    with_repeats = position_considered * sequence_repeats_needed
    return with_repeats[1:]


def run_fft(num_phases, input_list, part_num):
    list_to_alter = list(input_list)
    len_input = len(list_to_alter)
    for i in range(num_phases):
        if part_num == 2:
            print(f"Phase No. {i:>3}")
        output_list = list()
        for digit_position in range(len_input):
            if digit_position > len_input/2:
                sum_of = sum(list_to_alter[digit_position:])  # REDDIT RIPPED (No. 7)
            else:
                multiplications = map(mul, list_to_alter, return_repeating_pattern([0, 1, 0, -1], digit_position+1, len_input))
                sum_of = sum(multiplications)
            output_list.append(int(str(sum_of)[-1]))
        list_to_alter = list(output_list)

    if part_num == 1:
        return "".join([str(x) for x in list_to_alter[:8]])
    elif part_num == 2:
        message_offset = int("".join([str(x) for x in input_list[:7]]))
        return "".join([str(x) for x in list_to_alter[message_offset:message_offset+8]])


print("Part 1:", run_fft(100, split_input, 1))

print("Part 2:", run_fft(100, split_input * 10000, 2))
