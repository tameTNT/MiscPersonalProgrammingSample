from aocscrapper import get_AoC_input

if __name__ == '__main__':
    input_s = get_AoC_input(2020, 5).strip().split('\n')

    boarding_ids = set()
    for seat in input_s:
        row_list = list(range(128))
        column_list = list(range(8))
        for letter in seat:
            row_mid = len(row_list) // 2
            col_mid = len(column_list) // 2
            if letter == 'B':
                row_list = row_list[row_mid:]
            elif letter == 'F':
                row_list = row_list[:row_mid]

            elif letter == 'L':
                column_list = column_list[:col_mid]
            elif letter == 'R':
                column_list = column_list[col_mid:]

        seat_id = row_list[0] * 8 + column_list[0]

        boarding_ids.add(seat_id)

    min_id = min(boarding_ids)
    max_id = max(boarding_ids)
    
    print('Part 1:', max_id)

    all_possible_seats = set(range(min_id, max_id+1))
    print('Part 2:', all_possible_seats.difference(boarding_ids).pop())
