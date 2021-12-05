from aocscrapper import get_AoC_input
from itertools import permutations

days_input = get_AoC_input(2019, 7).strip().split(",")
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
        operands = input_instructions[index + 1:index + 4]
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
        operands = [input_instructions[index + 1]]
        mode_1 = False
        try:
            mode_1 = bool(int(subscriptable_number[-3]))
        except IndexError:
            pass
        modes = [mode_1]

    elif opcode == 5 or opcode == 6:
        operands = input_instructions[index + 1:index + 3]
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
    :param mode_bools: a list of booleans stating which parameters are using immediate mode (denoted True)
    :param operands: list of parameters
    :return: num based on mode for corresponding parameter
    """
    if mode_bools[index]:  # i.e. using immediate mode
        return operands[index]
    else:  # i.e. using position mode
        return input_instructions[operands[index]]


def execute_opcode(input_instructions, opcode, operands, operand_modes, opcode_3_input, instruction_pointer):
    """Executes a singular opcode on the input_instructions provided given the following parameters:

    :param input_instructions: program (list) to alter
    :param opcode: integer determining operation to use (i.e. opcode)
    :param operands: a list of the different parameters/operands of the operation
    :param operand_modes: list of booleans determining parameter/operand mode (immediate == True)
    :param opcode_3_input: the integer to submit as opcode_3 input (if requested)
    :param instruction_pointer: original value of instruction pointer to use
    :return: tuple containing description of rest of tuple (1/2 further values):
        "Instruction pointer + Input Confirm" - new instruction pointer; different description just allows input index for that amp to be changed
        "Instruction pointer + Output"  - new instruction pointer + output
        "Instruction pointer" - new instruction pointer
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
        return "Instruction pointer + Input Confirm", instruction_pointer + len(operands) + 1

    elif opcode == 4:  # OUTPUT
        return "Instruction pointer + Output", instruction_pointer + len(operands) + 1, operand_0

    elif opcode == 5 or opcode == 6:  # JUMP-IF-TRUE/JUMP-IF-FALSE
        operand_1 = return_mode_based_value(input_instructions, 1, operand_modes, operands)
        if (opcode == 5 and operand_0 != 0) or (opcode == 6 and operand_0 == 0):
            return "Instruction pointer", operand_1

    elif opcode == 7 or opcode == 8:  # LESS THAN/EQUALS
        operand_1 = return_mode_based_value(input_instructions, 1, operand_modes, operands)
        if (opcode == 7 and operand_0 < operand_1) or (opcode == 8 and operand_0 == operand_1):
            input_instructions[operands[2]] = 1
        else:
            input_instructions[operands[2]] = 0

    return "Instruction pointer", instruction_pointer + len(operands) + 1  #


class Amplifier:
    def __init__(self, starting_program):
        """Initialises an Amplifier object with:
        an intcode program, an instruction pointer (initially 0),  a list of outputs (from opcode 4) produced (initially empty)
        and an opcode3_input_index of 0.

        :param starting_program: the intcode program the amplifier should start fom - this is altered as opcodes are executed
        """
        self.intcode_program = starting_program
        self.instruction_pointer = 0
        self.outputs = list()
        self.opcode3_input_index = 0

    def run_intcode(self, opcode_3_input):
        """Runs the Amplifier's current intcode program continuing from the index of its current instruction_pointer.

        :param opcode_3_input: An list of the 2 inputs the program will need: the phase setting for the very first input
            and then the output of the previous amplifier in the chain for all subsequent inputs.
            Which one if used is determined by opcode3_input_index (this is changed to 1 once the first input opcode (3) has been processed)
        :return: Either:
            The result of an (opcode 4 induced) output or
            The string "Halted" if the program has reached a halt intcode (99)
        """
        while self.intcode_program[self.instruction_pointer] != 99:
            detail_dict = opcode_details(self.intcode_program, self.instruction_pointer)
            self.instruction_pointer = execute_opcode(self.intcode_program, detail_dict["opcode"],
                                                      detail_dict["operands"], detail_dict["operand modes"],
                                                      opcode_3_input[self.opcode3_input_index], self.instruction_pointer)

            if self.instruction_pointer[0] == "Instruction pointer + Output":
                result = self.instruction_pointer[2]
                self.outputs.append(result)
                self.instruction_pointer = self.instruction_pointer[1]
                return result
            elif self.instruction_pointer[0] == "Instruction pointer + Input Confirm":
                self.instruction_pointer = self.instruction_pointer[1]
                self.opcode3_input_index = 1
            elif self.instruction_pointer[0] == "Instruction pointer":
                self.instruction_pointer = self.instruction_pointer[1]

        return "Halted"


phase_setting_permutations = list(permutations(range(5, 10)))
potential_thruster_signals = list()

for perm in phase_setting_permutations:
    AmpA = Amplifier(list(days_input))  # All amplifiers re-instantiated to reset their intcode programs to defaults, outputs to empty and opcode3_input_index to 0
    AmpB = Amplifier(list(days_input))
    AmpC = Amplifier(list(days_input))
    AmpD = Amplifier(list(days_input))
    AmpE = Amplifier(list(days_input))

    E_output = 0
    while E_output != "Halted":
        A_output = AmpA.run_intcode([perm[0], E_output])
        B_output = AmpB.run_intcode([perm[1], A_output])
        C_output = AmpC.run_intcode([perm[2], B_output])
        D_output = AmpD.run_intcode([perm[3], C_output])
        E_output = AmpE.run_intcode([perm[4], D_output])
    potential_thruster_signals.append(AmpE.outputs[-1])

print("Part 2:", max(potential_thruster_signals))
