from aocscrapper import get_AoC_input
from math import atan, degrees

days_input = get_AoC_input(2019, 10).strip().split("\n")

grid_width = len(days_input[0])  # all rows are same width do only one line checked
grid_height = len(days_input)
coords_map = {(x, y): days_input[y][x] for y in range(grid_height) for x in range(grid_width)}
# Generates a list of the coordinates of all asteroids ('#') in the map given
asteroid_coords = [point for point in coords_map if coords_map[point] == "#"]
num_asteroids = len(asteroid_coords)

# A dictionary, added to later, with the number of other asteroids detectable from each asteroid
num_asteroids_detectable = {coords: int() for coords in asteroid_coords}
# A dictionary which contains a key for each individual asteroid. Value of each key is a dict with the angle between every other asteroid and this one
sight_line_angles = dict()

# Finds number of asteroids detectable from each separate asteroid coordinate
for (x, y) in asteroid_coords:
    # Creates a new dictionary with all the potential sight line angles (initially all angle value are blank)
    # between the current asteroid and all others, excluding the one to itself.
    # The zip object is simply a list of tuple pairs describing all the imaginary lines between the asteroid and all others (except itself).
    sight_line_angles[(x, y)] = {line: int() for line in zip([(x, y)]*(num_asteroids-1), [asteroid_coords[i] for i in range(num_asteroids) if asteroid_coords[i] != (x, y)])}

    # Gets the angle (starting at the vertical = 0 degrees) of the imaginary line connecting a pair of asteroids. Adds this angle to sight_line_angles[(x, y)] to 3 d.p.
    for line in sight_line_angles[(x, y)]:
        (coords1, coords2) = line  # unpacks pair of coordinates into two separate tuples
        (x1, y1), (x2, y2) = coords1, coords2  # unpacks these coordinates further into separate x and y values
        dy = y2 - y1
        dx = x2 - x1
        if dx == 0 and dy < 0:  # N
            angle_of_sight_line = 0
        elif dx > 0 and dy < 0:  # NE
            angle_of_sight_line = degrees(atan(dx/-dy))  # - in order to invert magnitude of dy or dx when less than 0
        elif dx > 0 and dy == 0:  # E
            angle_of_sight_line = 90
        elif dx > 0 and dy > 0:  # SE
            angle_of_sight_line = 90 + degrees(atan(dy/dx))
        elif dx == 0 and dy > 0:  # S
            angle_of_sight_line = 180
        elif dx < 0 and dy > 0:  # SW
            angle_of_sight_line = 180 + degrees(atan(-dx/dy))
        elif dx < 0 and dy == 0:  # W
            angle_of_sight_line = 270
        elif dx < 0 and dy < 0:  # NW
            angle_of_sight_line = 270 + degrees(atan(-dy/-dx))
        else:
            raise Exception("Invalid calculation of angle of sight line")

        sight_line_angles[(x, y)][line] = round(angle_of_sight_line, 3)

    # set() removes duplicates - simulating the fact that only one asteroid per sight line is detectable
    num_asteroids_detectable[(x, y)] = len(set(sight_line_angles[(x, y)].values()))

num_detectable_at_best_loc = max(num_asteroids_detectable.values())
print("Part 1:", num_detectable_at_best_loc)

# Retrieves the coordinates of the ideal monitoring station determined in Part 1
monitoring_station_coords = tuple()
for asteroid_coords in num_asteroids_detectable.keys():
    if num_asteroids_detectable[asteroid_coords] == num_detectable_at_best_loc:
        monitoring_station_coords = asteroid_coords

asteroids_to_shoot = sight_line_angles[monitoring_station_coords]
# creates a zip object of angles of asteroids and the target asteroid, then sorts this list by the angles (i.e. the first value in each tuple)
asteroid_angle_list = sorted(list(zip(asteroids_to_shoot.values(), [line[1] for line in asteroids_to_shoot.keys()])))
# Converts the above list (which contains repeating angle values) into a dictionary which states all the asteroids along a particular sight line/angle
angle_asteroid_dict = {angle: list() for angle in sorted(set(asteroids_to_shoot.values()))}
for asteroid in asteroid_angle_list:
    angle_asteroid_dict[asteroid[0]].append(asteroid[1])

# Rotates the imaginary laser along the sight lines/angles to destroy the asteroids
asteroids_destroyed = list()
xm, ym = monitoring_station_coords
asteroid_lines = list(angle_asteroid_dict.values())

while len(asteroids_destroyed) < 200:
    for asteroid_sight_line in asteroid_lines:  # iterates through all the 'sight lines' - serves as the rotation of the laser
        if asteroid_sight_line:  # i.e. are there asteroids remaining in this angle's sight line?
            distances_from_monitoring_station = {asteroid: int() for asteroid in asteroid_sight_line}

            # calculates distance from monitoring station to each asteroid in the firing line and saves result in dictionary created above
            for asteroid in asteroid_sight_line:
                xa, ya = asteroid
                dy, dx = (ya - ym), (xa - xm)
                distances_from_monitoring_station[asteroid] = (dy**2 + dx**2)**0.5

            shortest_distance = min(distances_from_monitoring_station.values())

            # finds the asteroid with the shortest distance then adds it to the asteroids_destroyed list
            # before removing it from the asteroid_sight_line list (since it is no longer in the sight line)
            for asteroid in asteroid_sight_line:
                if distances_from_monitoring_station[asteroid] == shortest_distance:
                    asteroids_destroyed.append(asteroid)
                    asteroid_sight_line.remove(asteroid)

two_hundredth_destroyed = asteroids_destroyed[199]
print("Part 2:", two_hundredth_destroyed[0]*100 + two_hundredth_destroyed[1])
