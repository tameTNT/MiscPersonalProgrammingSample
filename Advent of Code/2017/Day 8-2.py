import operator

# This is a lookup table used later int he program. The operator class is a 'functioned' version of the normal operators (>, <, >=, etc.)
# This table selectes the operator function relating to the string operator
operators = {">": operator.gt, "<": operator.lt, ">=": operator.ge, "<=": operator.le, "==": operator.eq, "!=": operator.ne}
# instructions = ["b inc 5 if a > 1", "a inc 1 if b < 5", "c dec -10 if a >= 1", "c inc -20 if c == 10"]
registers = {}
highest = 0

with open("Inputs\\Day 8 Input.txt") as input_set:
    for line in input_set:
        parts = line.strip("\n").split()

        if parts[0] not in registers:
            registers[parts[0]] = 0
        if parts[4] not in registers:
            registers[parts[4]] = 0

        # 1: looks up the string operator in the table; 2: that forms the 'base' of the function. The brackets then contain the arguments;
        # 3 & 4: These are the arguments for the operator function, i.e. the values a and b
        # ---------1----------2------------3---------------------4-------
        if operators[parts[5]](int(registers[parts[4]]), int(parts[6])):
            if parts[1] == "inc":
                registers[parts[0]] += int(parts[2])

            elif parts[1] == "dec":
                registers[parts[0]] -= int(parts[2])

        if max(registers.values()) > highest:
            highest = max(registers.values())

    #print(registers)
    print(highest)
