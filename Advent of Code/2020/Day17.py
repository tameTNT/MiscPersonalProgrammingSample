from aocscrapper import get_AoC_input
import time

if __name__ == '__main__':
    input_s = [list(x) for x in get_AoC_input(2020, 17, get_test=False).strip().split('\n')]

    active_set = set()
    for y in range(len(input_s)):
        for x in range(len(input_s[0])):
            if input_s[y][x] == '#':
                active_set.add((x, y, 0))  # input is only z=0 plane

    def simulate_step(space_set):
        all_x = [pos[0] for pos in space_set]
        all_y = [pos[1] for pos in space_set]
        all_z = [pos[2] for pos in space_set]

        x_range = range(min(all_x) - 1, max(all_x) + 2)
        y_range = range(min(all_y) - 1, max(all_y) + 2)
        z_range = range(min(all_z) - 1, max(all_z) + 2)

        new_state = set(space_set)
        for cube_coord in [(x, y, z) for z in z_range for y in y_range for x in x_range]:
            active_nearby_count = 0
            for z in (-1, 0, 1):
                for y in (-1, 0, 1):
                    for x in (-1, 0, 1):
                        if not (x == y == z == 0):
                            cx = cube_coord[0] + x
                            cy = cube_coord[1] + y
                            cz = cube_coord[2] + z
                            if (cx, cy, cz) in space_set:
                                active_nearby_count += 1

            if cube_coord in space_set:
                if active_nearby_count not in (2, 3):
                    new_state.remove(cube_coord)
            else:
                if active_nearby_count == 3:
                    new_state.add(cube_coord)

        return new_state

    for i in range(6):
        active_set = set(simulate_step(active_set))

    print('Part 1:', len(active_set))

    # PART 2 with w-plane
    active_set = set()
    for y in range(len(input_s)):
        for x in range(len(input_s[0])):
            if input_s[y][x] == '#':
                active_set.add((x, y, 0, 0))  # input is only z=0, w=0 plane


    def simulate_step(space_set):
        all_x = [pos[0] for pos in space_set]
        all_y = [pos[1] for pos in space_set]
        all_z = [pos[2] for pos in space_set]
        all_w = [pos[3] for pos in space_set]

        x_range = range(min(all_x) - 1, max(all_x) + 2)
        y_range = range(min(all_y) - 1, max(all_y) + 2)
        z_range = range(min(all_z) - 1, max(all_z) + 2)
        w_range = range(min(all_w) - 1, max(all_w) + 2)

        new_state = set(space_set)
        for cube_coord in [(x, y, z, w) for w in w_range for z in z_range for y in y_range for x in x_range]:
            active_nearby_count = 0
            for w in (-1, 0, 1):
                for z in (-1, 0, 1):
                    for y in (-1, 0, 1):
                        for x in (-1, 0, 1):
                            if not (x == y == z == w == 0):
                                cx = cube_coord[0] + x
                                cy = cube_coord[1] + y
                                cz = cube_coord[2] + z
                                cw = cube_coord[3] + w
                                if (cx, cy, cz, cw) in space_set:
                                    active_nearby_count += 1

            if cube_coord in space_set:
                if active_nearby_count not in (2, 3):
                    new_state.remove(cube_coord)
            else:
                if active_nearby_count == 3:
                    new_state.add(cube_coord)

        return new_state


    tic = time.perf_counter()
    for i in range(6):
        active_set = set(simulate_step(active_set))
    toc = time.perf_counter()

    print('Part 2:', len(active_set))
    print(f'Simulated six time-steps of four dimensional space in {toc-tic:.4f} seconds.')
