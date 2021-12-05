"""
https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
Make the initial cell the current cell and mark it as visited
While there are unvisited cells
    If the current cell has any neighbours which have not been visited
        Choose randomly one of the unvisited neighbours
        Push the current cell to the stack
        Remove the wall between the current cell and the chosen cell
        Make the chosen cell the current cell and mark it as visited
    Else if stack is not empty
        Pop a cell from the stack
        Make it the current cell
"""
import random


# Prints the maze as a grid
def print_grid():
    for i in range(len(grid)):
        print("".join(grid[i]))


# Changes the symbol at a coordinate in the grid/maze. ~ is used for unvisited cells, 'a space' for visited (the maze's actual path) and # is used for walls
def change_at_coor(x, y, operation_type):
    if operation_type == "cell_creation":
        grid[x][y] = "~"  # grid is a 2D list so needs two slices
    if operation_type == "visited":
        grid[x][y] = " "
    if operation_type == "entrance/exit":
        grid[x][y] = ">"


# Checks whether there are any unvisited cells (~) in the grid. Returns True is there are
def check_unvisited():
    done = False
    for r in range(rows):
        for c in range(columns):
            if grid[r][c] == "~":
                done = True
    return done


# Checks for unvisited cells in the 4 directions from the current cell
def neighbors():
    global stack  # The stack is added to so needs to be global
    options = []  # Options list holds the possible cells the maze could continue to
    currentx = current_cell[0]
    currenty = current_cell[1]

    # The if statements check for unvisited cells below, above, left and right
    if currenty - 2 >= 0:  # These if statements make sure the index isn't negative (which python would still accept - logic error)
        if grid[currentx][currenty-2] == "~":
            options.append([currentx, currenty-2])  # If the cell/neighbor passes all the tests then it gets appended to the possible choices

    if currenty + 2 < columns:
        if grid[currentx][currenty + 2] == "~":
            options.append([currentx, currenty+2])

    if currentx - 2 >= 0:
        if grid[currentx-2][currenty] == "~":
            options.append([currentx-2, currenty])

    if currentx + 2 < rows:
        if grid[currentx+2][currenty] == "~":
            options.append([currentx+2, currenty])

    if not options:  # i.e. There were no unvisited neighbors and options list is empty
        choice = stack.pop(random.randrange(0, len(stack)))  # Selects a random cell from the stack(past visited cells)
        return choice

    else:
        choice = options[random.randrange(0, len(options))]  # Chooses a random direction to go in
        break_walls(current_cell, choice)  # Calls on the function to create the actual maze path
        stack.append(current_cell)  # Adds the current to cell to stack so it can be backtracked to
        return choice


# Breaks the wall between the two chosen cells, the current and selected neighbor
def break_walls(original, destination):
    xdif = original[0] - destination[0]
    ydif = original[1] - destination[1]
    if xdif == -2:  # This means the break goes eastwards
        change_at_coor(original[0]+1, original[1], "visited")
    elif xdif == 2:  # westwards
        change_at_coor(original[0]-1, original[1], "visited")
    elif ydif == -2:  # southwards
        change_at_coor(original[0], original[1]+1, "visited")
    elif ydif == 2:  # northwards
        change_at_coor(original[0], original[1]-1, "visited")


# These should be odd numbers
rows = int(input("Enter the height of the maze "))
columns = int(input("Enter the width of the maze "))
if rows % 2 == 0:  # Makes sure that the numbers inputted are odd
    rows += 1
if columns % 2 == 0:
    columns += 1

# Starting coordinates for the maze algorithm
startx = 1
starty = 1

# Generates the plain grid for the maze as a 2D list
grid = [["#" for c in range(columns)] for r in range(rows)]

# Resets common variables
current_cell = [startx, starty]
stack = []

# Creates the cells within the grid
for row in range(rows):
    if row % 2 == 1:
        for column in range(columns):
            if column % 2 == 1:
                change_at_coor(row, column, "cell_creation")

# Sets the starting cell and sets it to 'visited'
change_at_coor(startx, starty, "visited")

# Main program loop
while check_unvisited():
    current_cell = neighbors()  # Neighbors returns the coordinates for the new current cell
    change_at_coor(current_cell[0], current_cell[1], "visited")  # This then calls on the function to change them

# Adds an entrance/exit to the maze in the top left and bottom right, shown by a >. These can be anywhere as the maze is just one route
change_at_coor(1, 0, "entrance/exit")
change_at_coor(rows-2, columns-1, "entrance/exit")

print_grid()  # Prints the final maze
print(grid)
print("".join(["".join(grid[row]) for row in range(len(grid))]))
