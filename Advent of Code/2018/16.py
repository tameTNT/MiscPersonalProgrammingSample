def addr(registera, registerb):
    return register_values[registera] + register_values[registerb]


def addi(registera, valueb):
    return register_values[registera] + valueb


def mulr(registera, registerb):
    return register_values[registera] * register_values[registerb]


def muli(registera, valueb):
    return register_values[registera] * valueb


def banr(registera, registerb):
    return register_values[registera] & register_values[registerb]


def bani(registera, valueb):
    return register_values[registera] & register_values[valueb]


def borr(registera, registerb):
    return register_values[registera] | register_values[registerb]


def bori(registera, valueb):
    return register_values[registera] | valueb


def setr(registera):
    return register_values[registera]


def seti(valuea):
    return valuea


def gtir(valuea, registerb):
    if valuea > register_values[registerb]:
        return 1
    else:
        return 0


def gtri(registera, valueb):
    if register_values[registera] > valueb:
        return 1
    else:
        return 0


def gtrr(registera, registerb):
    if register_values[registera] > register_values[registerb]:
        return 1
    else:
        return 0


def egir(valuea, registerb):
    if valuea == register_values[registerb]:
        return 1
    else:
        return 0


def egri(registera, valueb):
    if register_values[registera] == valueb:
        return 1
    else:
        return 0


def egrr(registera, registerb):
    if register_values[registera] == register_values[registerb]:
        return 1
    else:
        return 0


with open("Inputs\\Day16.txt", "r") as input_set:
    read_input_set = input_set.read()
    part_inputs = [section.strip() for section in read_input_set.split("\n\n")]
    part_1_input = part_inputs[:-2]
    test_program_part2 = [[int(number) for number in line.split(" ")] for line in part_inputs[-1].split("\n")]
    register_values = [number for number in range(4)]
    part_1_overall_count = 0
    opcode_possibilities = {opcode: list() for opcode in range(16)}

    for sample in part_1_input:
        register_values = [int(value.strip("[]")) for value in sample.split("\n")[0].strip("Before:  ").split(",")]
        instructions = [int(instruction) for instruction in sample.split("\n")[1].split(" ")]
        after = [int(value.strip("[]")) for value in sample.split("\n")[2].strip("After:  ").split(",")]

        count = 0
        opcode, A, B, C = instructions[0], instructions[1], instructions[2], instructions[3]

        if addr(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("addr")
        if addi(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("addi")
        if mulr(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("mulr")
        if muli(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("muli")
        if banr(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("banr")
        if bani(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("bani")
        if borr(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("borr")
        if bori(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("bori")
        if setr(A) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("setr")
        if seti(A) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("seti")
        if gtir(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("gtir")
        if gtri(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("gtri")
        if gtrr(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("gtrr")
        if egir(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("egir")
        if egri(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("egri")
        if egrr(A, B) == after[C]:
            count += 1
            opcode_possibilities[opcode].append("egrr")

        if count >= 3:
            part_1_overall_count += 1

    print("Part 1: ", part_1_overall_count)
    """for opcode in opcode_possibilities:
        print("Part 2 (manual first part): ", opcode, set(opcode_possibilities[opcode]))"""
    # final_opcodes = {0: , 1: , 2: bani, 3: banr, 4: gtir, 5: setr, 6: , 7: egir, 8: seti, 9: , 10: egrr, 11: egri, 12: , 13: gtrr, 14: mulr, 15: gtri}  # Determined from above - WORK ON THIS

    final_opcodes = {i: None for i in range(16)}
    opcode_possibilities = {opcode: set(opcode_possibilities[opcode]) for opcode in range(16)}
    print(opcode_possibilities)
    print(opcode_possibilities[0].intersection(opcode_possibilities[5]))
