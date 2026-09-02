"""
recorder.py
Remembering every move the pen makes, and playing those moves back.

Written by Elchin.
"""


def record_point(points, pen, colour, size, pen_is_down):
    """Add the pen's current position and settings to the end of the list."""
    points.append({
        "x": pen.xcor(),
        "y": pen.ycor(),
        "colour": colour,
        "size": size,
        "pen_down": pen_is_down,
    })


def replay_drawing(pen, points):
    """Clear the screen, then draw every saved point again in order."""
    pen.clear()
    pen.penup()

    for point in points:
        pen.pencolor(point["colour"])
        pen.pensize(point["size"])

        if point["pen_down"]:
            pen.pendown()
        else:
            pen.penup()

        pen.goto(point["x"], point["y"])


def undo_last(pen, points):
    """Remove the most recent point, then draw what is left."""
    if len(points) > 1:
        points.pop()

    replay_drawing(pen, points)
