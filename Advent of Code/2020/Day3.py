from aocscrapper import get_AoC_input

if __name__ == '__main__':
    input_s = [list(y) for y in get_AoC_input(2020, 3).strip().split('\n')]
    grid_width = len(input_s[0])

    def test_slope(dx, dy):
        num_trees = 0
        for y in range(len(input_s)//dy):
            if input_s[y * dy][(y * dx) % grid_width] == '#':
                num_trees += 1

        return num_trees

    print('Part 1:', test_slope(3, 1))
    print('Part 2:', test_slope(1, 1)*test_slope(3, 1)*test_slope(5, 1)*test_slope(7, 1)*test_slope(1, 2))
