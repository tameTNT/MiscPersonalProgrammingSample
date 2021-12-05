from aocscrapper import get_AoC_input

days_input = get_AoC_input(2019, 2).strip().split(",")
days_input = [int(x) for x in days_input]


def return_opcode_and_indexes(input_instructions, index):
    return input_instructions[index:index + 4]


def operation(input_instructions, operation_opcode, parameter_1, parameter_2):
    if operation_opcode == 1:
        return input_instructions[parameter_1] + input_instructions[parameter_2]

    if operation_opcode == 2:
        return input_instructions[parameter_1] * input_instructions[parameter_2]


def run_intcode_program(part_input):
    global instruction_pointer
    while part_input[current_index] != 99:
        opcode, index_one, index_two, result_index = return_opcode_and_indexes(part_input, current_index)
        part_input[result_index] = operation(part_input, opcode, index_one, index_two)
        current_index += 4


p1_input = list(days_input)  # overrides pointers and actually creates a new list instance
p1_input[1] = 12
p1_input[2] = 2
instruction_pointer = 0
run_intcode_program(p1_input)
print(f"Part 1: {p1_input[0]}")

found = False
for noun in range(0, 100):
    if not found:
        for verb in range(0, 100):
            if not found:
                instruction_pointer = 0
                p2_input = list(days_input)  # resets memory
                p2_input[1] = noun
                p2_input[2] = verb
                run_intcode_program(p2_input)

                if p2_input[0] == 19690720:
                    print(f"Part 2: {100 * noun + verb}")
                    found = True
