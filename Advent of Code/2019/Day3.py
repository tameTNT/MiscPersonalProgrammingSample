from aocscrapper import get_AoC_input

days_input = get_AoC_input(2019, 3)  # Test input: "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83\n"
days_input = days_input.strip().split("\n")
wire_description = [wire.split(",") for wire in days_input]
wire_coords_and_lengths = {0: dict(), 1: dict()}

for wire_number in range(len(wire_description)):
    current_coordinates = [0, 0]  # Each wire starts at centre of grid
    length = 0
    for instruction in wire_description[wire_number]:
        direction = instruction[0]
        distance = int(instruction[1:])
        for i in range(distance):
            if direction == "R":
                current_coordinates[0] -= 1
            elif direction == "L":
                current_coordinates[0] += 1
            elif direction == "D":
                current_coordinates[1] -= 1
            elif direction == "U":
                current_coordinates[1] += 1

            length += 1

            coords_tuple = tuple(current_coordinates)
            if coords_tuple not in wire_coords_and_lengths[wire_number].keys():
                wire_coords_and_lengths[wire_number][coords_tuple] = length

wire_one_coords = set(wire_coords_and_lengths[0].keys())
wire_two_coords = set(wire_coords_and_lengths[1].keys())
# Faster because entire list does not need to be searched, only hash location checked - takes ms rather than mins!
intersection_coords = wire_one_coords.intersection(wire_two_coords)  # REDDIT RIPPED (No. 1)

distances_from_start = [abs(x) + abs(y) for (x, y) in intersection_coords]
print("Part 1:", min(distances_from_start))

wire_lengths = [wire_coords_and_lengths[0][coords] + wire_coords_and_lengths[1][coords] for coords in intersection_coords]  # REDDIT RIPPED (No. 2)
print("Part 2:", min(wire_lengths))
