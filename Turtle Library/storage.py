"""
storage.py
Saving drawings to JSON files and loading them back.

Written by Aytaj.
"""

import json
import os
from datetime import datetime


FOLDER = "drawings"


def save_drawing(points):
    """Write the list of points to a new JSON file.
    The file name contains the date and time, so nothing is overwritten."""
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)

    # A set collects each colour only once, no matter how often it was used
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
    """Read one JSON file and return only the list of points."""
    path = os.path.join(FOLDER, filename)

    with open(path) as file:
        drawing = json.load(file)

    return drawing["points"]


def list_drawings():
    """Return the names of all saved drawings, oldest first."""
    if not os.path.exists(FOLDER):
        return []

    # List comprehension: keep only the files that end in .json
    names = [name for name in os.listdir(FOLDER) if name.endswith(".json")]

    # Lambda: sort by the file name in lower case
    return sorted(names, key=lambda name: name.lower())
