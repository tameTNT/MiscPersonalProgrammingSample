# "0 3 0 1 -3"
instructions = []

with open("Inputs\\Day 5 Input.txt") as input_set:
    for line in input_set:
        instructions.append(int(line.strip()))

    # instructions = instructions.split(" ")
    # instructions = [int(x) for x in instructions]
    instruction_pointer = 0
    counter = 0

    while True:
        if instruction_pointer >= len(instructions) or instruction_pointer < 0:
            print("Escaped")
            break

        counter += 1
        value_to_change = instruction_pointer
        instruction_pointer += instructions[instruction_pointer]
        instructions[value_to_change] += 1

print(counter)
