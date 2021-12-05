from aocscrapper import get_AoC_input

days_input = get_AoC_input(2019, 5).strip().split(",")
days_input = [int(x) for x in days_input]


def opcode_details(input_instructions, index):
    """
    :param input_instructions: program list to work from
    :param index: index of opcode
    :return: dictionary containing opcode, (modes of parameters/operands (list)), parameters/operands
    """
    subscriptable_number = str(input_instructions[index])
    opcode = int(subscriptable_number[-1])

    operands = list()
    modes = list()
    
    if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
        operands = input_instructions[index+1:index + 4]
        mode_1 = False
        mode_2 = False
        mode_3 = False
        try:
            mode_1 = bool(int(subscriptable_number[-3]))
            mode_2 = bool(int(subscriptable_number[-4]))
            mode_3 = bool(int(subscriptable_number[-5]))
        except IndexError:  # These try except statements are to catch if leading zeros have been removed
            pass
        modes = [mode_1, mode_2, mode_3]

    elif opcode == 3 or opcode == 4:
        operands = [input_instructions[index+1]]
        mode_1 = False
        try:
            mode_1 = bool(int(subscriptable_number[-3]))
        except IndexError:
            pass
        modes = [mode_1]

    elif opcode == 5 or opcode == 6:
        operands = input_instructions[index+1:index+3]
        mode_1 = False
        mode_2 = False
        try:
            mode_1 = bool(int(subscriptable_number[-3]))
            mode_2 = bool(int(subscriptable_number[-4]))
        except IndexError:
            pass
        modes = [mode_1, mode_2]

    return {"opcode": opcode, "operand modes": modes, "operands": operands}


def return_mode_based_value(input_instructions, index, mode_bools, operands):
    """
    :param input_instructions: program list to grab values from if necessary
    :param index: index of value in parameters that is being considered
    :param mode_bools: tuple of booleans stating which parameters are using immediate mode (denoted True)
    :param operands: list of parameters
    :return: num based on mode for corresponding parameter
    """
    if mode_bools[index]:  # i.e. using immediate mode
        return operands[index]
    else:  # i.e. using position mode
        return input_instructions[operands[index]]


def execute_opcode(input_instructions, opcode, operand_modes, operands, opcode_3_input, instruction_pointer):
    """
    :param input_instructions: program (list) to alter
    :param opcode: integer determining operation to use (i.e. opcode)
    :param operand_modes: list of booleans determining parameter/operand mode (immediate = True)
    :param operands: a list of the different parameters/operands of the operation
    :param opcode_3_input: the integer to submit as opcode_3 input if requested
    :param instruction_pointer: current value of instruction pointer
    :return: new instruction pointer value
    """
    # used in almost every opcode so declared here
    operand_0 = return_mode_based_value(input_instructions, 0, operand_modes, operands)

    if opcode == 1 or opcode == 2:
        operand_1 = return_mode_based_value(input_instructions, 1, operand_modes, operands)

        if opcode == 1:  # ADDITION
            input_instructions[operands[2]] = operand_0 + operand_1
        elif opcode == 2:  # MULTIPLICATION
            input_instructions[operands[2]] = operand_0 * operand_1

    elif opcode == 3:  # INPUT
        input_instructions[operands[0]] = opcode_3_input

    elif opcode == 4:  # OUTPUT
        print(operand_0)

    elif opcode == 5 or opcode == 6:  # JUMP-IF-TRUE/JUMP-IF-FALSE
        operand_1 = return_mode_based_value(input_instructions, 1, operand_modes, operands)
        if (opcode == 5 and operand_0 != 0) or (opcode == 6 and operand_0 == 0):
            return operand_1

    elif opcode == 7 or opcode == 8:  # LESS THAN/EQUALS
        operand_1 = return_mode_based_value(input_instructions, 1, operand_modes, operands)
        if (opcode == 7 and operand_0 < operand_1) or (opcode == 8 and operand_0 == operand_1):
            input_instructions[operands[2]] = 1
        else:
            input_instructions[operands[2]] = 0

    return instruction_pointer + len(operands) + 1  # REDDIT RIPPED (post completion) (No. 3)


def run_intcode(input_program, opcode_3_input):
    instruction_pointer = 0
    while input_program[instruction_pointer] != 99:
        detail_dict = opcode_details(input_program, instruction_pointer)
        instruction_pointer = execute_opcode(input_program, detail_dict["opcode"], detail_dict["operand modes"], detail_dict["operands"],
                                             opcode_3_input, instruction_pointer)


print("Part 1 (ignore 0 debug codes): ")
run_intcode(list(days_input), 1)

print("Part 2: ")
run_intcode(list(days_input), 5)
