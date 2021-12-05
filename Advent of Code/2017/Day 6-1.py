with open("Inputs\\Day 6 Input.txt") as input_set:
    for line in input_set:
        instructions = line.strip().split()
        instructions = [int(x) for x in instructions]
        past_combinations = []
        counter = 0

        while True:
            biggest_index = instructions.index(max(instructions))
            amount = instructions[biggest_index]
            instructions[biggest_index] = 0

            for i in range(biggest_index+1, amount+biggest_index+1):
                instructions[i % len(instructions)] += 1

            counter += 1

            if instructions in past_combinations:
                print(counter)
                break
            else:
                past_combinations.append(list(instructions))
