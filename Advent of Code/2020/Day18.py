from aocscrapperCOPY import get_AoC_input
import re

if __name__ == '__main__':
    input_s = [x for x in get_AoC_input(2020, 18, get_test=False).strip().split('\n')]

    def resolve(e, part2=False):
        while '(' in e or ')' in e:
            innermost_brackets = re.findall(r'\(([^(][^()]*[^)])\)', e)
            for part in innermost_brackets:
                sub_result = str(resolve(part, part2))
                e = e.replace(f'({part})', sub_result)

        in_order_val_opp = [n for n in e.split(' ')]
        while len(in_order_val_opp) >= 3:
            if not part2 or '+' not in in_order_val_opp:
                in_order_val_opp.insert(3, str(eval(''.join(in_order_val_opp[:3]))))
                for i in range(3):
                    in_order_val_opp.pop(0)
            else:
                addition_index = in_order_val_opp.index('+')
                in_order_val_opp.insert(addition_index+2, str(eval(''.join(in_order_val_opp[addition_index-1:addition_index+2]))))
                for i in range(3):
                    in_order_val_opp.pop(addition_index - 1)

        return int(in_order_val_opp[0])  # there should only be one value remaining in the list

    line_sum = 0
    for equ in input_s:
        line_sum += resolve(equ)
    print('Part 1:', line_sum)

    line_sum = 0
    for equ in input_s:
        line_sum += resolve(equ, True)
    print('Part 2:', line_sum)
