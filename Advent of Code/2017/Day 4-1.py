counter = 0  # aa bb cc dd ee

with open("Inputs\\Day 4 Input.txt") as input_set:
    for line in input_set:
        input_list = line.strip().split(" ")
        words = []
        valid = True
        for item in input_list:
            if item in words:
                valid = False
                break
            else:
                words.append(item)

        if valid:
            counter += 1

print(counter)
