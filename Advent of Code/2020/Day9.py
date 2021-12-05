from aocscrapper import get_AoC_input

if __name__ == '__main__':
    input_s = [int(x) for x in get_AoC_input(2020, 9).strip().split('\n')]

    def find_pair(target, ilist):  # from day 1
        diff_table = dict()
        for val in ilist:
            if val in diff_table.keys():
                return True
            else:
                diff_table[target - val] = val

        return False  # if no pair found

    preamble_len = 25

    for i in range(preamble_len, len(input_s)):
        if not find_pair(input_s[i], input_s[i-preamble_len:i]):
            invalid_num = input_s[i]
            print('Part 1:', invalid_num)
            break

    found = False
    for i in range(preamble_len, len(input_s)):
        if not found:
            for j in range(0, i-1):  # j-1 ensures sublists are at minimum 2 long
                contiguous_set = input_s[j:i]
                sum_trial = sum(contiguous_set)
                if sum_trial < invalid_num:
                    break
                elif sum_trial == invalid_num:
                    print('Part 2:', max(contiguous_set) + min(contiguous_set))
                    found = True
                    break
        else:
            break
