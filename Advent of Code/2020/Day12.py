from aocscrapper import get_AoC_input
import math

if __name__ == '__main__':
    input_s = [(x[0], int(x[1:])) for x in get_AoC_input(2020, 12).strip().split('\n')]

    location = [0, 0]
    heading = 1  # N:0, E:1, S:2, W:3
    for instruction in input_s:
        action = instruction[0]
        value = instruction[1]

        if action == 'N':
            location[1] += value
        elif action == 'E':
            location[0] += value
        elif action == 'S':
            location[1] -= value
        elif action == 'W':
            location[0] -= value
        elif action == 'L':
            heading -= value // 90
            heading %= 4
        elif action == 'R':
            heading += value // 90
            heading %= 4
        elif action == 'F':
            if heading == 0:
                location[1] += value
            elif heading == 1:
                location[0] += value
            elif heading == 2:
                location[1] -= value
            elif heading == 3:
                location[0] -= value

    print('Part 1:', abs(location[0]) + abs(location[1]))

    def rotate_waypoint(start, degree):
        # applying a rotation matrix
        angle = math.radians(degree)
        # int() truncates 0.9999999 in some cases
        return [round(start[0] * math.cos(angle) - start[1] * math.sin(angle)),
                round(start[0] * math.sin(angle) + start[1] * math.cos(angle))]

    location = [0, 0]
    waypoint = [10, 1]
    for instruction in input_s:
        action = instruction[0]
        value = instruction[1]

        if action == 'N':
            waypoint[1] += value
        elif action == 'E':
            waypoint[0] += value
        elif action == 'S':
            waypoint[1] -= value
        elif action == 'W':
            waypoint[0] -= value
        elif action == 'L':
            waypoint = rotate_waypoint(list(waypoint), value)
        elif action == 'R':
            waypoint = rotate_waypoint(list(waypoint), -value)
        elif action == 'F':
            location[0] += waypoint[0] * value
            location[1] += waypoint[1] * value

    print('Part 2:', abs(location[0]) + abs(location[1]))
