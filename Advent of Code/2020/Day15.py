from aocscrapper import get_AoC_input
import time

if __name__ == '__main__':
    input_s = [int(x) for x in get_AoC_input(2020, 15, get_test=False).strip().split(',')]

    recent_dict = dict()

    tic = time.perf_counter()

    turn_num = 0
    for starting_num in input_s:
        turn_num += 1
        recent_dict[starting_num] = turn_num
        last = starting_num

    while turn_num < 30000000:
        turn_num += 1
        turn_value = int()

        if last not in recent_dict:
            turn_value = 0
        else:
            turn_diff = (turn_num-1) - recent_dict[last]
            turn_value = turn_diff

        recent_dict[last] = turn_num - 1
        last = turn_value

        if turn_num == 2020:
            print('Part 1:', last)
        elif turn_num == 30000000:
            toc = time.perf_counter()

            print('Part 2:', last)
            print(f'\nPlayed 30000000 turn game in {toc - tic:.4f} seconds')
