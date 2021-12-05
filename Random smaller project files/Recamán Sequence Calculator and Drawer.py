import turtle


def draw_recaman_sequence(bgcolor="purple", screen_size_x=1000, screen_size_y=1000, pen_width=1, speed=1000, drawing_size=5, angle=45, nth_term=1000):
    recaman = turtle.Turtle()
    canvas = turtle.Screen()

    recaman.penup()
    canvas.screensize(screen_size_x, screen_size_y)
    canvas.bgcolor("black")
    recaman.hideturtle()
    recaman.setpos(-(screen_size_x / 2), -(screen_size_y / 2))  # Sets the turtle position to the bottom left
    recaman.pensize(pen_width)  # Determines the pen width
    recaman.color("white")
    recaman.pendown()
    recaman.speed(speed)  # Determines the speed at which the sequence is drawn

    current = 0
    sequence = []

    for i in range(nth_term):  # The nth term to be generated up to
        taken_away = current - i
        added = current + i
        radius = i / 2 * drawing_size

        if (taken_away not in sequence) and (taken_away >= 0):
            current = taken_away
            sequence.append(current)
            recaman.setheading(90+angle)  # +45 sets the drawing on a 45 degree angle; same in future uses
            if i % 2 == 0:
                recaman.circle(radius, 180)
            else:
                recaman.circle(radius, -180)
        else:
            current = added
            sequence.append(added)
            recaman.setheading(90+angle)
            if i % 2 == 0:
                recaman.circle(-radius, 180)
            else:
                recaman.circle(-radius, -180)

    canvas.bgcolor(bgcolor)  # This is to show that the program has finished
    canvas.exitonclick()  # Turtle window exits when you click it
    return sequence  # First 50 terms: 0, 1, 3, 6, 2, 7, 13, 20, 12, 21, 11, 22, 10, 23, 9, 24, 8, 25, 43, 62, 42, 63, 41, 18, 42, 17, 43, 16, 44, 15, 45, 14, 46, 79, 113, 78, 114, 77, 39, 78, 38, 79, 37, 80, 36, 81, 35, 82, 34, 83


print(draw_recaman_sequence(screen_size_x=200, screen_size_y=200, nth_term=100))
