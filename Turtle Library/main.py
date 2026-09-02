"""
main.py
Turtle Etch-A-Sketch  -  Group 2, Project 1.1

Controls
    Arrow keys   move the pen
    1 to 5       change colour
    + and -      change pen size
    space        lift or lower the pen
    u            undo the last move
    c            clear the drawing
    s            save the drawing to a JSON file
    l            load the newest saved drawing and replay it

Written by Ilaha.
"""

import turtle

import canvas
import artist
import storage
import recorder


WIDTH = 900
HEIGHT = 650

# ---------------------------------------------------------------
# The state of the program
# ---------------------------------------------------------------
points = []                              # every place the pen has been
current_colour = canvas.DEFAULT_COLOUR
current_size = 3
pen_is_down = True


# ---------------------------------------------------------------
# Set up the window
# ---------------------------------------------------------------
screen = turtle.Screen()
screen.title("Group 2  -  Turtle Etch-A-Sketch")
screen.bgcolor("white")
screen.setup(width=1000, height=750)

canvas.draw_frame(WIDTH, HEIGHT)

pen = artist.make_pen()
label = artist.make_label()


# ---------------------------------------------------------------
# Two small helpers used by almost every key
# ---------------------------------------------------------------
def save_point():
    """Ask Elchin's module to remember where the pen is now."""
    recorder.record_point(points, pen, current_colour, current_size, pen_is_down)


def update_status():
    """Refresh the text at the top of the window."""
    artist.show_status(label, current_colour, current_size, pen_is_down)


def apply_settings():
    """Put the pen back to the current colour, size, and up or down state.
    Needed after a replay, because replay leaves the pen on the last saved point."""
    pen.pencolor(current_colour)
    pen.pensize(current_size)

    if pen_is_down:
        pen.pendown()
    else:
        pen.penup()


# ---------------------------------------------------------------
# What the keys do
# ---------------------------------------------------------------
def move(direction):
    """Move the pen one step and remember the new position."""
    artist.move_pen(pen, direction)
    save_point()


def set_colour(key):
    """Change the drawing colour."""
    global current_colour
    current_colour = canvas.get_colour(key)
    pen.pencolor(current_colour)
    update_status()


def change_size(amount):
    """Make the pen thicker or thinner, but keep it between 1 and 10."""
    global current_size
    current_size = current_size + amount

    if current_size < 1:
        current_size = 1
    elif current_size > 10:
        current_size = 10

    pen.pensize(current_size)
    update_status()


def toggle_pen():
    """Lift the pen if it is down, lower it if it is up."""
    global pen_is_down
    pen_is_down = not pen_is_down
    apply_settings()
    update_status()


def undo():
    """Take back the last move."""
    recorder.undo_last(pen, points)
    apply_settings()


def clear_all():
    """Throw the drawing away and start again in the middle."""
    global points
    points = []

    pen.clear()
    pen.penup()
    pen.home()
    apply_settings()
    save_point()
    update_status()


def save():
    """Write the drawing to a JSON file."""
    path = storage.save_drawing(points)
    print("Saved", len(points), "points to", path)


def load():
    """Load the newest saved drawing and draw it again."""
    global points

    names = storage.list_drawings()

    if len(names) == 0:
        print("There are no saved drawings yet.")
        return

    newest = names[-1]
    points = storage.load_drawing(newest)

    print("Replaying", newest, "with", len(points), "points")
    recorder.replay_drawing(pen, points)
    apply_settings()


# ---------------------------------------------------------------
# One small function for each key
#
# onkey can only call a function that takes no arguments.
# Our move, set_colour and change_size functions all need a value,
# so we give each key its own little function that supplies it.
# ---------------------------------------------------------------
def move_up():
    move("up")


def move_down():
    move("down")


def move_left():
    move("left")


def move_right():
    move("right")


def use_black():
    set_colour("1")


def use_red():
    set_colour("2")


def use_blue():
    set_colour("3")


def use_green():
    set_colour("4")


def use_orange():
    set_colour("5")


def thicker():
    change_size(1)


def thinner():
    change_size(-1)


# ---------------------------------------------------------------
# Connect the keys to the functions
# ---------------------------------------------------------------
screen.listen()

screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

screen.onkey(use_black, "1")
screen.onkey(use_red, "2")
screen.onkey(use_blue, "3")
screen.onkey(use_green, "4")
screen.onkey(use_orange, "5")

screen.onkey(thicker, "plus")
screen.onkey(thinner, "minus")

screen.onkey(toggle_pen, "space")
screen.onkey(undo, "u")
screen.onkey(clear_all, "c")
screen.onkey(save, "s")
screen.onkey(load, "l")


# ---------------------------------------------------------------
# Start
# ---------------------------------------------------------------
save_point()        # remember the starting position
update_status()

screen.mainloop()   # keep the window open until the user closes it