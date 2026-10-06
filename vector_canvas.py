import tkinter as tk
from pathlib import Path

from code_5_3 import readPolylineFile


WIDTH = 900
HEIGHT = 600
PADDING = 40

input_file = (
    Path(__file__).resolve().parent / "data" / "polylines.txt"
)
polylines, _ = readPolylineFile(input_file)

all_points = [
    point
    for polyline in polylines
    for point in polyline.points
]

xmin = min(point.x for point in all_points)
xmax = max(point.x for point in all_points)
ymin = min(point.y for point in all_points)
ymax = max(point.y for point in all_points)

if xmin == xmax or ymin == ymax:
    raise ValueError("Координатын мужийн өргөн, өндөр тэг байж болохгүй")


def toScreen(point):
    draw_width = WIDTH - 2 * PADDING
    draw_height = HEIGHT - 2 * PADDING

    xscreen = (
        PADDING
        + (point.x - xmin) / (xmax - xmin) * draw_width
    )
    yscreen = (
        PADDING
        + draw_height
        - (point.y - ymin) / (ymax - ymin) * draw_height
    )

    return xscreen, yscreen


root = tk.Tk()
root.title("Lab03 — Vector Data Visualization")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    background="white",
)
canvas.pack()

for number, polyline in enumerate(polylines, start=1):
    screen_points = [toScreen(point) for point in polyline.points]
    coordinates = [
        value
        for screen_point in screen_points
        for value in screen_point
    ]

    first = polyline.points[0]
    last = polyline.points[-1]
    is_closed = (
        len(polyline.points) >= 4
        and first.x == last.x
        and first.y == last.y
    )

    if is_closed:
        canvas.create_polygon(
            *coordinates,
            fill="#c8e6c9",
            outline="#2e7d32",
            width=2,
        )
    else:
        canvas.create_line(
            *coordinates,
            fill="#1565c0",
            width=3,
        )

    for x, y in screen_points:
        canvas.create_oval(
            x - 3, y - 3,
            x + 3, y + 3,
            fill="red",
            outline="red",
        )

    x, y = screen_points[0]
    canvas.create_text(
        x + 8,
        y - 12,
        text=f"Feature {number}",
        anchor="w",
    )

canvas.create_text(
    WIDTH / 2,
    15,
    text="Blue: polyline | Green: polygon | Red: vertices",
)

root.mainloop()