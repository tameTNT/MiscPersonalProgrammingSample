total = 0

with open("Inputs\\Day 2 Input.txt") as input_set:
    for line in input_set:
        line = line.strip()
        line_numbers = line.split()
        line_numbers = [int(x) for x in line_numbers]
        found_pair = False

        for number_1 in line_numbers:
            for number_2 in line_numbers:
                if number_1 % number_2 == 0 and number_1 != number_2:
                    found_pair = True
                    break

            if found_pair:
                line_division = number_1 / number_2
                break

        total += line_division

print(total)
