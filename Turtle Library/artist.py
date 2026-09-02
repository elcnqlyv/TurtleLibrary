"""
artist.py
The drawing pen, how it moves, and the status line at the top.

Written by Aydan.
"""

import turtle


STEP = 20  # how far one arrow key press moves the pen

# Direction name  ->  angle in degrees
HEADINGS = {
    "up": 90,
    "down": 270,
    "left": 180,
    "right": 0,
}


def make_pen():
    """Create the turtle that does the drawing and return it."""
    pen = turtle.Turtle()
    pen.shape("turtle")
    pen.speed(0)
    pen.pensize(3)
    return pen


def make_label():
    """Create a second turtle that only writes the status line."""
    label = turtle.Turtle()
    label.hideturtle()
    label.penup()
    label.goto(-430, 300)
    return label


def move_pen(pen, direction):
    """Point the pen in one of four directions, then move it one step."""
    pen.setheading(HEADINGS[direction])
    pen.forward(STEP)


def show_status(label, colour, size, pen_is_down):
    """Erase the old status line and write a new one."""
    label.clear()

    if pen_is_down:
        state = "DOWN"
    else:
        state = "UP"

    text = "Colour: " + colour + "    Size: " + str(size) + "    Pen: " + state
    label.write(text, font=("Courier", 14, "normal"))
