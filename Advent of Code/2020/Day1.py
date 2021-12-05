from aocscrapper import get_AoC_input

if __name__ == '__main__':
    input_s = [int(x) for x in get_AoC_input(2020, 1).strip().split('\n')]


    def find_pair(target, ilist):
        diff_table = dict()
        for val in ilist:
            if val in diff_table.keys():
                return val * diff_table[val]
            else:
                diff_table[target - val] = val

        return None  # if no pair found


    print('Part 1:', find_pair(2020, input_s))  # 1016964

    for x in input_s:
        res = find_pair(2020-x, input_s)  # returns product of pair that sum to 2020-val
        if res:  # if such as pair exists
            print('Part 2:', x * res)  # 182588480
            break
