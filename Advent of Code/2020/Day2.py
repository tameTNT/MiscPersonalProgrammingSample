from aocscrapper import get_AoC_input
from collections import Counter

if __name__ == '__main__':
    input_s = [[pol.strip(':') for pol in x.split(' ')] for x in get_AoC_input(2020, 2).strip().split('\n')]

    valid_count = 0
    for password in input_s:
        count = Counter(password[2])
        policy = password[1]
        min_pol = int(password[0].split('-')[0])
        max_pol = int(password[0].split('-')[1])

        count = dict(count.most_common())
        if policy in count.keys():
            if min_pol <= count[policy] <= max_pol:
                valid_count += 1

    print('Part 1:', valid_count)  # 396

    valid_count = 0
    for password in input_s:
        policy = password[1]
        min_pol_index = int(password[0].split('-')[0]) - 1  # indexes start at 1 (not 0)
        max_pol_index = int(password[0].split('-')[1]) - 1
        if bool(password[2][min_pol_index] == policy) != bool(password[2][max_pol_index] == policy):  # XOR operation
            valid_count += 1

    print('Part 2:', valid_count)
