from aocscrapper import get_AoC_input

if __name__ == '__main__':
    # gets input and pads with floor spaces around the outside
    input_s = ['.'+x+'.' for x in get_AoC_input(2020, 11).strip().split('\n')]
    g_width = len(input_s[0])
    input_s.insert(0, '.' * g_width)
    input_s.append('.' * g_width)
    g_height = len(input_s)

    input_grid = dict()
    for y in range(g_height):
        for x in range(g_width):
            input_grid[(x, y)] = input_s[y][x]


    def check_neighbours(grid, centre, part2):
        occupied_count = 0
        cx = centre[0]
        cy = centre[1]

        if not part2:
            # +++
            # +@+
            # +++
            if grid[(cx+1, cy)] == '#':
                occupied_count += 1
            if grid[(cx+1, cy+1)] == '#':
                occupied_count += 1
            if grid[(cx, cy+1)] == '#':
                occupied_count += 1
            if grid[(cx-1, cy+1)] == '#':
                occupied_count += 1
            if grid[(cx-1, cy)] == '#':
                occupied_count += 1
            if grid[(cx-1, cy-1)] == '#':
                occupied_count += 1
            if grid[(cx, cy-1)] == '#':
                occupied_count += 1
            if grid[(cx+1, cy-1)] == '#':
                occupied_count += 1

        elif part2:
            # looking left
            x = cx - 1
            while x > 0:
                seat = grid[(x, cy)]
                if seat == 'L':
                    break
                elif seat == '.':
                    x -= 1
                elif seat == '#':
                    occupied_count += 1
                    break

            # looking right
            x = cx + 1
            while x < g_width:
                seat = grid[(x, cy)]
                if seat == 'L':
                    break
                elif seat == '.':
                    x += 1
                elif seat == '#':
                    occupied_count += 1
                    break

            # looking up
            y = cy - 1
            while y > 0:
                seat = grid[(cx, y)]
                if seat == 'L':
                    break
                elif seat == '.':
                    y -= 1
                elif seat == '#':
                    occupied_count += 1
                    break

            # looking down
            y = cy + 1
            while y < g_height:
                seat = grid[(cx, y)]
                if seat == 'L':
                    break
                elif seat == '.':
                    y += 1
                elif seat == '#':
                    occupied_count += 1
                    break

            # looking up-left
            x = cx - 1
            y = cy - 1
            while x > 0 and y > 0:
                seat = grid[(x, y)]
                if seat == 'L':
                    break
                elif seat == '.':
                    y -= 1
                    x -= 1
                elif seat == '#':
                    occupied_count += 1
                    break

            # looking up-right
            x = cx + 1
            y = cy - 1
            while x < g_width and y > 0:
                seat = grid[(x, y)]
                if seat == 'L':
                    break
                elif seat == '.':
                    y -= 1
                    x += 1
                elif seat == '#':
                    occupied_count += 1
                    break

            # looking down-left
            x = cx - 1
            y = cy + 1
            while x > 0 and y < g_height:
                seat = grid[(x, y)]
                if seat == 'L':
                    break
                elif seat == '.':
                    y += 1
                    x -= 1
                elif seat == '#':
                    occupied_count += 1
                    break

            # looking down-right
            x = cx + 1
            y = cy + 1
            while x < g_width and y < g_height:
                seat = grid[(x, y)]
                if seat == 'L':
                    break
                elif seat == '.':
                    y += 1
                    x += 1
                elif seat == '#':
                    occupied_count += 1
                    break

        return occupied_count

    def simulate(start_grid, part2=False):
        input_grid = dict(start_grid)
        if part2:
            tolerance = 5
        else:
            tolerance = 4

        i = 0
        while True:
            i += 1
            if i % 10 == 0:
                print('On simulation iteration', i, end='\r')

            transaction_dict = dict(input_grid)
            for y in range(1, g_height-1):
                for x in range(1, g_width-1):
                    if input_grid[(x, y)] == 'L':
                        if check_neighbours(input_grid, (x, y), part2) == 0:
                            transaction_dict[(x, y)] = '#'
                    elif input_grid[(x, y)] == '#':
                        if check_neighbours(input_grid, (x, y), part2) >= tolerance:
                            transaction_dict[(x, y)] = 'L'

            if transaction_dict == input_grid:
                occupied_count = 0
                for y in range(g_height):
                    for x in range(g_width):
                        if input_grid[(x, y)] == '#':
                            occupied_count += 1

                return occupied_count

            else:
                input_grid = dict(transaction_dict)

                # if part2:
                #     print_string = str()
                #     for y in range(g_height):
                #         for x in range(g_width):
                #             print_string += input_grid[(x, y)]
                #         print_string += '\n'
                #
                #     print(print_string)


    print('Part 1:', simulate(input_grid))
    print('Part 2:', simulate(input_grid, part2=True))
