"""
canvas.py
Colours and the frame around the drawing area.

Written by Gadir.
"""

import turtle


# Keyboard key  ->  colour name
COLOURS = {
    "1": "black",
    "2": "red",
    "3": "blue",
    "4": "green",
    "5": "orange",
}

DEFAULT_COLOUR = "black"


def get_colour(key):
    """Return the colour for a number key.
    If the key is not in the dictionary, return the default colour."""
    if key in COLOURS:
        return COLOURS[key]
    else:
        return DEFAULT_COLOUR


def draw_frame(width, height):
    """Draw a grey rectangle around the drawing area.
    This uses its own turtle, so clearing the drawing does not erase it."""
    frame = turtle.Turtle()
    frame.hideturtle()
    frame.speed(0)
    frame.pencolor("grey")
    frame.pensize(3)

    frame.penup()
    frame.goto(-width / 2, height / 2)
    frame.pendown()

    for i in range(2):
        frame.forward(width)
        frame.right(90)
        frame.forward(height)
        frame.right(90)
