with open("Inputs\\Day10.txt", "r") as input_set:
	notes = [line.strip() for line in input_set]
	notes = [note.split("v") for note in notes]
	notes = [[note[0].split("=")[1].strip(), note[1].split("=")[1].strip()] for note in notes]
	stars = dict()
	velocities = dict()
	
	for i in range(len(notes)):
		stars[i] = [int(coord) for coord in notes[i][0].strip("<>").split(",")]
		velocities[i] = [int(velocity) for velocity in notes[i][1].strip("<>").split(",")]

	found = False
	for time in range(20000):  # 20000 just to make sure the text is found, once text has been found loops are simply skipped
		if not found:
			x_values = [coord[0] for coord in stars.values()]
			biggest_x = max(x_values)
			smallest_x = min([coord[0] for coord in stars.values()])
			y_values = [coord[1] for coord in stars.values()]
			biggest_y = max(y_values)
			smallest_y = min(y_values)

			if biggest_x - smallest_x < 65:  # a little over 6 (letter width) * 8 (number of letters) + 2*8 (spaces)
				picture = str()
				star_positions = stars.values()
				for Y in range(smallest_y, biggest_y+1):
					for X in range(smallest_x, biggest_x+1):
						if [X, Y] in star_positions:
							picture += "#"
						else:
							picture += "."
					picture += "\n "
				
				print("Part 1: \n", picture)
				print("Part 2: ", time)
				found = True

			for i in range(len(stars)):
				stars[i][0] += velocities[i][0]
				stars[i][1] += velocities[i][1]
