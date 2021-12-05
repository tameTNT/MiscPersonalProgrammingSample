from aocscrapper import get_AoC_input
# from timeit import timeit
'''Sick Reddit solution (Py 3.8):
for i in range(lower, upper + 1):
    if (s := str(i)) == "".join(sorted(s)):
        c = set(Counter(s).values())

        part_one += bool(c & {2 ,3, 4, 5, 6})
        part_two += bool(c & {2})'''

days_input = get_AoC_input(2019, 4).strip().split("-")


def group_digits(str_num):
    all_digitgroups = list()

    one_digitgroup = str()
    for i in range(len(str_num)):
        if one_digitgroup == "":  # i.e. if a group of numbers has just been finished and one_digitgroup cleared
            one_digitgroup += str_num[i]

        if i == len(str_num)-1:  # i.e. if last digit, makes sure current grouping is actually added
            all_digitgroups.append(one_digitgroup)
        else:  # normally (i.e. before last digit is reached)
            if str_num[i] == str_num[i+1]:
                one_digitgroup += str_num[i+1]
            else:
                all_digitgroups.append(one_digitgroup)
                one_digitgroup = ""  # resets/clears one_digitgroup string

    return all_digitgroups


def possible_password(password, part_2=1):
    ascending = True
    double_found = False

    last_digit = 0
    for digit in password:
        digit = int(digit)
        if last_digit > digit:  # checks if each digit is same or larger than previous digit
            ascending = False
            break
        last_digit = digit

    if ascending:  # Reduces execution time significantly as only passwords that match the first criteria are 'grouped'
        for grouping in group_digits(password):
            if part_2 and len(grouping) == 2:  # only groups of numbers exactly 2 long are accepted in part 2
                double_found = True
            elif not part_2 and len(grouping) >= 2:  # any group of numbers (i.e. length>1) accepted in part 1
                double_found = True

    if double_found and ascending:
        return True
    else:
        return False


# print(timeit(lambda: [group_digits(str(123456))], number=100000))

start = int(days_input[0])
end = int(days_input[1])
for part in (0, 1):  # acts like (False, True) but allows for having a part number printed easily
    possibilities = 0
    for num in range(start, end+1):
        if possible_password(str(num), part_2=part):
            possibilities += 1

    print(f"Part {part+1}: {possibilities}")
