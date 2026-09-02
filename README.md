# Group 2 — Turtle Etch-A-Sketch, how to explain your code

One section per person, in presentation order. Ilaha opens with the architecture, hands off to each of you, then closes with the main program and the demo.

Run it with `python3 main.py` from inside the project folder. That matters — the imports break if you run it from somewhere else.

---

## 0. Words you will use

**Module** — a `.py` file you can import into another one. We wrote four of our own.

**Function** — a named block of code you run later by writing its name. Takes things in (parameters), hands something back (return value).

**Dictionary** — a lookup table. `COLOURS["2"]` gives back `"red"`. Written with curly brackets and colons.

**List** — an ordered collection you can add to. Written with square brackets.

---

## 1. Gadir — `canvas.py`

### Your code

```python
COLOURS = {
    "1": "black",
    "2": "red",
    "3": "blue",
    "4": "green",
    "5": "orange",
}

DEFAULT_COLOUR = "black"


def get_colour(key):
    if key in COLOURS:
        return COLOURS[key]
    else:
        return DEFAULT_COLOUR


def draw_frame(width, height):
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
```

### How to read it out loud

We define a dictionary called `COLOURS`. On the left of each colon is a key on the keyboard, written as a string. On the right is the colour name that key should give us. So pressing 2 means red.

We define a variable called `DEFAULT_COLOUR` and set it to black. This is what we fall back to.

Then we define a function called `get_colour` that takes one parameter, `key`. Inside, we check whether that key exists in the dictionary. If it does, we return the colour stored under it. If it does not, we return the default colour instead. That way an unknown key can never crash the program.

Then we define a second function called `draw_frame`, which takes a width and a height.

Inside, we create a brand new turtle called `frame`. We hide it so the arrow shape does not sit on the border. We set its speed to zero, which in turtle means as fast as possible. We set the colour to grey and the pen thickness to 3.

We lift the pen, move to the top left corner, and put the pen back down. Moving with the pen up means we travel without leaving a line.

Then a loop. `range(2)` gives us two passes. Each pass draws one long side and one short side, turning right 90 degrees after each. Two passes draw all four sides of the rectangle.

### The one idea to land

`draw_frame` creates its own turtle on purpose. The drawing pen gets cleared every time the user presses undo or replay. If the frame were drawn by that same pen, it would vanish too.

### If they ask

**"Why not just write `if key == "1"` five times?"** Because then adding a sixth colour means adding another `if`. With a dictionary, you add one line and everything else keeps working — including the loop in `main.py` that creates the key bindings.

**"What does `range(2)` do?"** It gives the loop two turns. We draw two sides per turn, so four sides in total.

---

## 2. Aydan — `artist.py`

### Your code

```python
STEP = 20

HEADINGS = {
    "up": 90,
    "down": 270,
    "left": 180,
    "right": 0,
}


def make_pen():
    pen = turtle.Turtle()
    pen.shape("turtle")
    pen.speed(0)
    pen.pensize(3)
    return pen


def make_label():
    label = turtle.Turtle()
    label.hideturtle()
    label.penup()
    label.goto(-430, 300)
    return label


def move_pen(pen, direction):
    pen.setheading(HEADINGS[direction])
    pen.forward(STEP)


def show_status(label, colour, size, pen_is_down):
    label.clear()

    if pen_is_down:
        state = "DOWN"
    else:
        state = "UP"

    text = "Colour: " + colour + "    Size: " + str(size) + "    Pen: " + state
    label.write(text, font=("Courier", 14, "normal"))
```

### How to read it out loud

We define a variable called `STEP` and set it to 20. That is how many pixels the pen travels for one arrow key press. It is written once here, so changing this single number changes the whole app.

We define a dictionary called `HEADINGS`. On the left is a direction name, on the right is the angle in degrees that turtle uses. In turtle, zero degrees points right, 90 points up, 180 points left, 270 points down.

Then `make_pen`. We create a new turtle, give it the turtle shape so the user can see where the pen is, set speed to zero, set the thickness to 3, and return it.

Then `make_label`. We create a second turtle. We hide it, because it only writes text and we do not want an arrow sitting next to the words. We lift its pen so it does not draw a line on the way, and move it to the top left of the window. Then we return it.

Then `move_pen`, which takes the pen and a direction name. We look the direction up in the dictionary to get an angle, and `setheading` points the turtle at that angle. Then `forward(STEP)` moves it 20 pixels that way.

Then `show_status`. First we clear whatever the label wrote before, otherwise the new text would print on top of the old one. Then we check whether the pen is down and store the word DOWN or UP in a variable called `state`. Then we build one long string by joining the pieces with plus signs. `str(size)` is there because size is a number and you cannot add a number to a string. Finally `write` puts that text on the screen in the font we chose.

### The one idea to land

We use two separate turtles. One draws, one writes. They are independent, so clearing the drawing never wipes the status line, and updating the status line never touches the drawing.

### If they ask

**"What is `setheading`?"** It points the turtle at an absolute angle, regardless of where it was facing before. That is what makes this an Etch-A-Sketch — up always means up. `left()` and `right()` would turn it relative to its current direction instead.

**"Why `str(size)`?"** Because `size` is a number and the rest is text. Python will not add the two types together. `str()` converts the number into text first.

---

## 3. Aytaj — `storage.py`

### Your code

```python
import json
import os
from datetime import datetime

FOLDER = "drawings"


def save_drawing(points):
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)

    colours_used = {point["colour"] for point in points}

    drawing = {
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "point_count": len(points),
        "colours_used": sorted(colours_used),
        "points": points,
    }

    filename = "drawing_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    path = os.path.join(FOLDER, filename)

    with open(path, "w") as file:
        json.dump(drawing, file, indent=2)

    return path


def load_drawing(filename):
    path = os.path.join(FOLDER, filename)

    with open(path) as file:
        drawing = json.load(file)

    return drawing["points"]


def list_drawings():
    if not os.path.exists(FOLDER):
        return []

    names = [name for name in os.listdir(FOLDER) if name.endswith(".json")]

    return sorted(names, key=lambda name: name.lower())
```

### How to read it out loud

We import three modules. `json` reads and writes JSON files. `os` talks to the file system. From `datetime` we bring in the `datetime` class, which gives us the current time.

We define a variable called `FOLDER` holding the folder name, so it is written once and reused everywhere.

**`save_drawing`.** It takes the list of points.

First we check whether the folder exists. `os.path.exists` returns true or false, and `not` flips it, so this reads as "if the folder does not exist". In that case `os.mkdir` creates it. Without this, saving would crash the very first time anyone runs the app.

Then we build a set called `colours_used`. The curly brackets with a `for` inside make a set comprehension. It walks every point and collects the colour. A set keeps each value only once, so even if we used red two hundred times, red appears in the set once.

Then we build a dictionary called `drawing` with four entries. The time we saved it, formatted by `strftime` into a readable string. How many points there are, using `len`. The colours used, sorted into alphabetical order. And the points themselves.

Then we build a file name that contains the date and time, so every save creates a new file instead of overwriting the last one. `os.path.join` glues the folder and the file name together with the right separator for the operating system.

Then `with open(path, "w") as file` opens the file for writing. The `with` form closes the file automatically when the block ends, even if something goes wrong. `json.dump` writes our dictionary into it, and `indent=2` makes the file readable rather than one long line.

Finally we return the path so `main.py` can print where the drawing went.

**`load_drawing`.** Takes a file name, builds the full path, opens the file for reading, and `json.load` turns the text back into a Python dictionary. We return only the points, because that is all the rest of the program needs.

**`list_drawings`.** If the folder does not exist yet, we return an empty list so nothing crashes.

Then a list comprehension. Read it as: for every name in the folder, keep it if it ends in `.json`. It builds a new list in one line. The long form would be an empty list, a `for` loop, an `if`, and an `append` — four lines instead of one.

Then we return that list sorted. The `key` parameter tells `sorted` what to compare, and we pass a lambda — a small unnamed function that takes a name and gives back its lower case version. So sorting ignores capital letters.

### The one idea to land

The JSON file is readable. Open it in any text editor and you can see every point: its position, its colour, its size, and whether the pen was down. The drawing is data, not a picture, which is exactly why we can replay it.

### If they ask

**"Why a set and not a list for the colours?"** Because we want to know *which* colours appeared, not how many times. A set removes the duplicates for us with no extra code.

**"What is a lambda?"** A function written in one line without a name, used where a full `def` would be overkill. `lambda name: name.lower()` does the same job as a two-line function that takes a name and returns it in lower case.

**"Why does the file name have a timestamp?"** So each save is its own file. `list_drawings` sorts them, and because the timestamp is at the front, the newest one ends up last.

---

## 4. Elchin — `recorder.py`

### Your code

```python
def record_point(points, pen, colour, size, pen_is_down):
    points.append({
        "x": pen.xcor(),
        "y": pen.ycor(),
        "colour": colour,
        "size": size,
        "pen_down": pen_is_down,
    })


def replay_drawing(pen, points):
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
    if len(points) > 1:
        points.pop()

    replay_drawing(pen, points)
```

### How to read it out loud

**`record_point`** takes five parameters: the list we are adding to, the pen itself, and the three settings the pen is using right now.

Inside, we call `append` on the list, and what we append is a dictionary describing the pen at this moment. `pen.xcor()` and `pen.ycor()` read the turtle's coordinates. The other three values are handed to us by the caller.

This one function is what makes save, load, undo and replay possible. Everything else is built on top of it.

**`replay_drawing`** takes the pen and a list of points.

First we clear the screen, so we draw onto a blank canvas rather than on top of what is there. Then we lift the pen, so the very first move does not leave a stray line from wherever the turtle happened to be.

Then a loop over the points. Each point is a dictionary, so we pull values out by name.

We set the colour stored in this point. We set the thickness stored in this point. Then we check the `pen_down` value: if it is true we lower the pen, otherwise we lift it. Finally we go to the coordinates stored in this point.

Each point remembers not just where the pen was, but how the pen was set up when it got there. So replaying the list reproduces the drawing exactly, including the colour changes and the gaps where the user lifted the pen.

**`undo_last`** takes the pen and the points list.

We check there is more than one point. `pop()` removes the last item from a list, so this deletes the most recent move. The check stops us emptying the list completely, because we always keep the starting position.

Then we call `replay_drawing` on what is left. We do not erase one line segment. We throw the picture away and redraw it from the shortened list.

### The two ideas to land

**The drawing is a list, not a picture.** Everything the app does works because we kept the points. A picture you can only look at. A list you can rewind.

**Undo reuses replay.** Undo is two lines because replay already existed. Remove the last point, redraw. That is the payoff of keeping the two jobs separate.

### If they ask

**"Why does `record_point` take so many parameters?"** So this module owns no state of its own. It is handed everything it needs and gives back nothing. That makes it easy to test, and it is why we could check it worked without ever opening a turtle window.

**"Why clear the screen before replaying?"** Because otherwise the replay would draw on top of the existing picture and you would see both at once.

**"Why redraw everything for one undo?"** Turtle cannot erase a single line. Once ink is on the canvas, the only way to remove it is `clear()`. Since we still have the list, redrawing is straightforward and always correct.

**"Is that slow?"** For a few hundred points, no. For thousands we would turn the animation off during the redraw and back on at the end.

---

## 5. Ilaha — `main.py`

This is the file that runs. It imports the other four modules and wires them together. As main presenter you should introduce this file first at a high level, then come back to it at the end for the detail and the demo.

### The imports

```python
import turtle

import canvas
import artist
import storage
import recorder
```

We import turtle, then our own four modules. Only this file imports them. They do not know about each other, so the dependencies all run one way and you can read any single module on its own.

### The state

```python
points = []
current_colour = canvas.DEFAULT_COLOUR
current_size = 3
pen_is_down = True
```

Four variables holding everything the program needs to remember. An empty list for the points. The starting colour, taken from Gadir's module rather than typed again here. A starting thickness of 3. And a flag saying the pen starts down.

These sit outside every function, so any function can read them.

### The setup

```python
screen = turtle.Screen()
screen.title("Group 2  -  Turtle Etch-A-Sketch")
screen.bgcolor("white")
screen.setup(width=1000, height=750)

canvas.draw_frame(WIDTH, HEIGHT)

pen = artist.make_pen()
label = artist.make_label()
```

We create the screen object, set its title and background colour, and set the window size. Then we call Gadir's function to draw the frame, and Aydan's two functions to create the drawing pen and the status label.

### The three helpers

```python
def save_point():
    recorder.record_point(points, pen, current_colour, current_size, pen_is_down)
```

A short wrapper around Elchin's function. His module does not know about our variables, so we pass them in. Writing it once here means the five places that record a point stay short.

```python
def update_status():
    artist.show_status(label, current_colour, current_size, pen_is_down)
```

Another wrapper, this time around Aydan's function.

```python
def apply_settings():
    pen.pencolor(current_colour)
    pen.pensize(current_size)

    if pen_is_down:
        pen.pendown()
    else:
        pen.penup()
```

This one matters. After a replay, the pen is sitting on the last saved point with whatever colour and size that point used. Our variables still hold what the user chose. This function puts the pen back in step with them.

### The `global` keyword

```python
def set_colour(key):
    global current_colour
    current_colour = canvas.get_colour(key)
    pen.pencolor(current_colour)
    update_status()
```

`global` tells Python we mean `current_colour` from the top of the file, not a new one. Without it, assigning inside the function would create a separate variable that disappears when the function ends, and the colour would never actually change.

Worth noting: `save_point` does not need `global`, because it only reads the variables. `global` is only required when you assign a new value.

### Binding keys

```python
screen.listen()

screen.onkey(lambda: move("up"), "Up")
screen.onkey(lambda: set_colour("1"), "1")

screen.onkey(toggle_pen, "space")
```

`screen.listen()` tells the window to pay attention to the keyboard. Without it nothing responds.

`onkey` takes two things: a function to run, and the name of a key. The function must take no arguments. `move` needs to know which direction and `set_colour` needs to know which key, so we wrap each in a lambda that takes nothing and supplies the argument for us.

`toggle_pen` takes no arguments already, so we pass it directly. Note there are no brackets after it. Writing `toggle_pen()` would call the function immediately and hand `onkey` the result instead of the function itself. That is a common mistake and it fails silently.

### The last lines

```python
save_point()
update_status()

screen.mainloop()
```

We record the starting position, so replay has somewhere to begin. We draw the status line for the first time.

`mainloop()` hands control to turtle. It keeps the window open and watches for key presses until the user closes it. Nothing written after this line would ever run.

### If they ask

**"Why is the state at module level instead of in a class?"** For a program this size, module-level variables are simpler to read. A class would be right if we had several drawings open at once.

**"What happens if two keys are pressed at once?"** Turtle handles them one after another. There is no threading here, so the state can never be half-updated.

**"Why wrap Elchin's function instead of calling it directly?"** Because the call needs five arguments and it appears in five places. The wrapper puts that list in one spot, so if the point format ever changes we edit one line.

---

## 6. Requirements checklist

Bring this up if the instructor asks what you covered.

| Requirement | Where |
|---|---|
| Two control structures | `for` loops in `canvas.py`, `recorder.py`, `main.py`; `if`/`else` in all five files |
| Lists, tuples, sets, dictionaries | list of points, dictionary per point, `COLOURS` and `HEADINGS` dictionaries, set of colours in `storage.py`, tuple for the font |
| Two extra libraries | `json`, `os`, `datetime` — three |
| Two user-defined functions | fourteen across five files |
| Comments and consistent style | docstring at the top of every file and every function |
| User interaction | the whole app is keyboard driven |
| Advanced structures | list comprehension and set comprehension in `storage.py`, lambdas in `storage.py` and `main.py` |
| Real data structures | JSON files in the `drawings` folder |
| Own modules | `canvas.py`, `artist.py`, `storage.py`, `recorder.py` |
| Realistic use case | a drawing tool that saves its work and can replay it |

---

## 7. Rehearsal checklist

- [ ] Everyone has run `python3 main.py` on their own machine at least once
- [ ] Everyone can read their own code aloud without stopping to work out a line
- [ ] Someone has opened a saved JSON file in a text editor and looked at it
- [ ] The save, clear, replay sequence is rehearsed — that is the moment people remember
- [ ] You know which folder to run from, because the imports depend on it