total = 0

with open("Inputs\\Day 2 Input.txt") as input_set:
    for line in input_set:
        line = line.strip()
        line_numbers = line.split()
        line_numbers = [int(x) for x in line_numbers]
        line_numbers.sort()
        line_range = line_numbers[-1] - line_numbers[0]
        total += line_range

print(total)
