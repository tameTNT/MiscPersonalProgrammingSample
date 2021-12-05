from aocscrapper import get_AoC_input
import matplotlib.pyplot as plt
import numpy as np

days_input = get_AoC_input(2019, 11).strip().split(",")
days_input = [int(x) for x in days_input]
days_input += [0] * 1000  # adding padding to end of intcode program


def opcode_details(input_instructions, index):
    """
    :param input_instructions: program list to work from
    :param index: index of opcode
    :return: dictionary containing opcode, (modes of parameters/operands (list)), parameters/operands
    """
    subscriptable_number = str(input_instructions[index]).zfill(5)  # adds leading zeros back in
    opcode = int(subscriptable_number[-2:])  # last two digits of subscriptable_number (e.g. 03) form opcode
    modes = [int(x) for x in list(subscriptable_number)][:-2][::-1]  # gets integers; takes off opcode; reverses list to get appropriate order

    if opcode in (1, 2, 7, 8):  # opcodes with 3 parameters
        operands = input_instructions[index + 1:index + 4]
    elif opcode in (5, 6):  # opcodes with 2 parameters
        operands = input_instructions[index + 1:index + 3]
    elif opcode in (3, 4, 9):  # opcodes with 1 parameter
        operands = [input_instructions[index + 1]]
    else:
        raise Exception(f"Invalid opcode at index {index}")

    return {"opcode": opcode, "operand modes": modes, "operands": operands}


def return_mode_based_value(input_instructions, mode, operand, relative_base):
    """
    :param input_instructions: program list to grab values from if necessary
    :param mode: integer stating which mode operand value is using
    :param operand: operand value being considered
    :param relative_base: current value of relative_base - used for relative mode if required
    :return: appropriate value (from input_instructions or operands) for mode argument specified
    """
    if mode == 2:  # relative mode
        return input_instructions[operand+relative_base]
    elif mode == 1:  # immediate mode
        return operand
    elif mode == 0:  # position mode
        return input_instructions[operand]
    else:
        raise Exception("Invalid parameter mode")


def write_value(input_instructions, mode, write_index, value_to_write, relative_base):
    """Actually alters the values in input_instructions based on other arguments.

    :param input_instructions: intcode program to alter
    :param mode: mode of writing instruction - integer with value of either 0 (position) or 2 (relative)
    :param write_index: the index position of input_instructions to edit (may be altered by relative_base for relative mode)
    :param value_to_write: actual integer value to write to final index location within program
    :param relative_base: the current value of the relative base
    :return: None
    """
    if mode == 2:  # relative mode
        input_instructions[relative_base + write_index] = value_to_write
    elif mode == 0:  # position mode
        input_instructions[write_index] = value_to_write
    else:  # write operations can never use immediate mode
        raise Exception("Invalid parameter mode for write operation")


def execute_opcode(input_instructions, opcode, operands, operand_modes, opcode_3_input, instruction_pointer, relative_base):
    """Executes a singular opcode on the input_instructions provided given the following parameters:

    :param input_instructions: intcode program (list) to alter
    :param opcode: integer determining operation to use (i.e. opcode)
    :param operands: a list of the different parameters/operands of the operation
    :param operand_modes: list of integers determining parameter/operand mode
    :param opcode_3_input: the integer to submit as opcode 3 input (if requested)
    :param instruction_pointer: current value of instruction pointer
    :param relative_base: current value of relative base - used for relative parameter mode
    :return: tuple containing description of rest of tuple (1/2 further values):
        "Instruction pointer + Input Confirm" - new instruction pointer - different description just allows opcode3_input_index to be changed;
        "Instruction pointer + Output"  - new instruction pointer + output;
        "Instruction pointer" - new instruction pointer;
        "Instruction pointer + Relative Base adjust" - new instruction pointer - value to adjust relative_base by;
    """

    # used in almost every opcode so declared early here
    operand_0 = return_mode_based_value(input_instructions, operand_modes[0], operands[0], relative_base)

    new_ip = instruction_pointer + len(operands) + 1

    if opcode == 1 or opcode == 2:
        operand_1 = return_mode_based_value(input_instructions, operand_modes[1], operands[1], relative_base)
        if opcode == 1:  # ADDITION
            result = operand_0 + operand_1
        else:  # (opcode 2) MULTIPLICATION
            result = operand_0 * operand_1
        write_value(input_instructions, operand_modes[2], operands[2], result, relative_base)

    elif opcode == 3:  # INPUT
        write_value(input_instructions, operand_modes[0], operands[0], opcode_3_input, relative_base)
        return "Instruction pointer + Input Confirmation", new_ip

    elif opcode == 4:  # OUTPUT
        return "Instruction pointer + Output", new_ip, operand_0

    elif opcode == 5 or opcode == 6:  # JUMP-IF-TRUE/JUMP-IF-FALSE
        operand_1 = return_mode_based_value(input_instructions, operand_modes[1], operands[1], relative_base)
        if (opcode == 5 and operand_0 != 0) or (opcode == 6 and operand_0 == 0):
            new_ip = operand_1

    elif opcode == 7 or opcode == 8:  # LESS THAN/EQUALS
        operand_1 = return_mode_based_value(input_instructions, operand_modes[1], operands[1], relative_base)
        result = int((opcode == 7 and operand_0 < operand_1) or (opcode == 8 and operand_0 == operand_1))
        write_value(input_instructions, operand_modes[2], operands[2], result, relative_base)

    elif opcode == 9:  # RELATIVE BASE ADJUSTMENT
        return "Instruction pointer + Relative Base adjust", new_ip, operand_0

    else:
        raise Exception("Invalid opcode for execution")

    return "Just Instruction pointer", new_ip


class PaintingRobotBrain:
    def __init__(self, starting_program):
        """Initialises an object capable of running intcode with:
        an intcode program, an instruction pointer (initially 0),  an output list (produced by opcode 4) (initially empty)
        and an opcode3_input_index of 0.

        :param starting_program: the intcode program the instance should start with - this is altered as opcodes are executed
        """
        self.intcode_program = starting_program
        self.instruction_pointer = 0
        self.outputs = list()
        self.opcode3_input_index = 0
        self.relative_base = 0

    def run_intcode(self, opcode_3_input):
        """Runs the objects's current intcode program continuing from the index of its current instruction_pointer.

        :param opcode_3_input: A list of the inputs the program will request (opcode 3)
            Which one if used is determined by opcode3_input_index
            (its value is increased by 1 (mod length of list) for every input (opcode 3) processed)
        :return: Either:
            The result of an (opcode 4 induced) output or
            The string "Halted" if the program has reached a halt intcode (99)
        """
        while self.intcode_program[self.instruction_pointer] != 99:  # a halt instruction
            opcode_detail_dict = opcode_details(self.intcode_program, self.instruction_pointer)
            returned_values = execute_opcode(self.intcode_program, opcode_detail_dict["opcode"], opcode_detail_dict["operands"],
                                             opcode_detail_dict["operand modes"], opcode_3_input[self.opcode3_input_index],
                                             self.instruction_pointer, self.relative_base)

            self.instruction_pointer = returned_values[1]

            if returned_values[0] == "Instruction pointer + Output":
                result = returned_values[2]
                self.outputs.append(result)
                return result
            elif returned_values[0] == "Instruction pointer + Input Confirmation":
                self.opcode3_input_index = (self.opcode3_input_index + 1) % len(opcode_3_input)
            elif returned_values[0] == "Instruction pointer + Relative Base adjust":
                self.relative_base += returned_values[2]
            elif returned_values[0] == "Just Instruction pointer":
                pass
            else:
                raise Exception("Invalid return type string from execution of opcode")

        return "Halted"


def paint(painting_grid):
    current_robot_coords = [0, 0]
    current_robot_direction = 0  # i.e. north/upwards
    robot_processor = PaintingRobotBrain(list(days_input))
    panels_painted = set()  # set ensures duplicates are not counted

    output = None
    while output != "Halted":
        input_value = 0 if painting_grid[tuple(current_robot_coords)] == 0 else 1

        colour = robot_processor.run_intcode([input_value])
        if colour != "Halted":
            painting_grid[tuple(current_robot_coords)] = colour
            panels_painted.add(tuple(current_robot_coords))

        direction = robot_processor.run_intcode([input_value])
        if direction == 0:
            current_robot_direction = (current_robot_direction-90) % 360
        elif direction == 1:
            current_robot_direction = (current_robot_direction+90) % 360
        elif direction == "Halted":
            output = "Halted"
        else:
            raise Exception("Invalid direction output")

        if current_robot_direction == 0:  # N
            current_robot_coords[1] += 1
        elif current_robot_direction == 90:  # E
            current_robot_coords[0] += 1
        elif current_robot_direction == 180:  # S
            current_robot_coords[1] -= 1
        elif current_robot_direction == 270:  # W
            current_robot_coords[0] -= 1

    return panels_painted, painting_grid


grid = {(x, y): 0 for y in range(-100, 100) for x in range(-100, 100)}  # grid has to be quite large for part 1

print("Part 1:", len(paint(dict(grid))[0]))

part2_grid = dict(grid)
part2_grid[(0, 0)] = 1  # starting tile is white for part 2
painted_grid = paint(dict(part2_grid))[1]
# Converts the returned coords: colour dict into a list of just colour values (0s and 1s),
# reverses it (since coords originally go from -ve to +ve), turns it into a numpy array,
# reshapes it into an actual grid (200x200), then flips it in the y-axis (i.e. from left to right) ready for imshow()
displayable_grid = np.fliplr(np.array(list(painted_grid.values())[::-1]).reshape(200, 200))
plt.imshow(displayable_grid, cmap="binary")
print("Part 2: (see matplotlib window)")
plt.show()
