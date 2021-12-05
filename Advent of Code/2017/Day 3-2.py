# correct_sequence = [1,1,2,4,5,10,11,23,25,26,54,57,59,122,133,142,147,304,330,351,362,747,806]

distance = 1
direction = 90
coordinates = (0,0)
current_x = 0
current_y = 0

grid = {}
for x in range(-10,10):  # I just chose for the grid to be 20x20 (from -10 to 10 in both x and y)
    for y in range(-10,10):
        grid[x,y] = 0
grid[0,0] = 1

grid_values_list = []


def rotate():
    global direction
    direction -= 90  # The spiral is anti-clockwise
    if direction == -90:
        direction = 270
    
    
def set_value():
    # (x-1,y-1) (x,y-1) (x+1,y-1)
    # (x-1,y)   (x,y)   (x+1,y)
    # (x-1,y+1) (x,y+1) (x+1,y+1)
    grid[current_x, current_y] = grid[current_x+1, current_y]+grid[current_x+1, current_y+1]+grid[current_x, current_y+1]+grid[current_x-1, current_y+1]+grid[current_x-1, current_y]+grid[current_x-1, current_y-1]+grid[current_x, current_y-1]+grid[current_x+1, current_y-1]
    

for i in range(8):  # This can technically be any number greater than 7
    for i in range(2):  # Each distance occurs twice before the distance increases
        for i in range(distance):
            if direction == 0:
                current_y -= 1
            elif direction == 90:
                current_x += 1
            elif direction == 180:
                current_y += 1
            elif direction == 270:
                current_x -= 1
            set_value()
            grid_values_list.append(grid[current_x, current_y])
            
        rotate()
        
    distance += 1  # The distance increases by one every time
   
   
for number in grid_values_list:
    if number > 347991:  # My puzzle input
        print(number)  # The first printed value is the answer