def show_picture(canvas, darkest=1, origin="bottom"):
    """Draw a canvas. A square with 0 ink is white. A square with `darkest` ink or more is black.
    origin="bottom" puts row 0 at the bottom of the picture. origin="top" puts it at the top."""
    import matplotlib.pyplot as plt

    rows = len(canvas)
    columns = len(canvas[0])
    longest = max(rows, columns)
    size = min(7, max(3, longest / 5))
    # Scale the figure to the canvas so that every square stays square.
    plt.figure(figsize=(size * columns / longest, size * rows / longest))
    # "gray_r" draws 0 as white. vmin and vmax set which numbers are white and black.
    plt.imshow(canvas, cmap="gray_r", vmin=0, vmax=darkest, interpolation="nearest",
               origin="lower" if origin == "bottom" else "upper")
    # About ten labels along each edge, so a big canvas stays readable.
    plt.xticks(range(0, columns, max(1, columns // 10)))
    plt.yticks(range(0, rows, max(1, rows // 10)))


def make_canvas(rows, columns):
    canvas = []
    for row in range(rows):
        canvas.append([0] * columns)
    return canvas


def paint_point(canvas, row, column):
    canvas[row][column] = canvas[row][column] + 1


def paint_horizontal(canvas, row, start_column, end_column):
    for column in range(start_column, end_column + 1):
        paint_point(canvas, row, column)


def paint_vertical(canvas, column, start_row, end_row):
    for row in range(start_row, end_row + 1):
        paint_point(canvas, row, column)


def paint_rectangle(canvas, first_row, first_column, last_row, last_column):
    for row in range(first_row, last_row + 1):
        paint_horizontal(canvas, row, first_column, last_column)


def paint_square(canvas, row, column, size):
    paint_rectangle(canvas, row, column, row + size - 1, column + size - 1)


def paint_grid(canvas, spacing):
    rows = len(canvas)
    columns = len(canvas[0])
    for row in range(0, rows, spacing):
        paint_horizontal(canvas, row, 0, columns - 1)
    for column in range(0, columns, spacing):
        paint_vertical(canvas, column, 0, rows - 1)


def paint_fade(canvas, row, column, length):
    for step in range(length):
        canvas[row][column + step] = canvas[row][column + step] + (length - step)


def paint_gradient(canvas, first_row, first_column, last_row, last_column):
    height = last_row - first_row + 1
    for step in range(height):
        for column in range(first_column, last_column + 1):
            canvas[first_row + step][column] = canvas[first_row + step][column] + (step + 1)


def paint_xy(canvas, x, y):
    """Paint the square at (x, y). With origin="bottom", (0, 0) is the bottom-left square and y is the row."""
    # A row of -1 would quietly wrap to the last row, so test both ends.
    if 0 <= y < len(canvas) and 0 <= x < len(canvas[0]):
        paint_point(canvas, y, x)


def paint_line(canvas, a, b, start_x, end_x):
    if abs(a) <= 1:
        for x in range(start_x, end_x + 1):
            paint_xy(canvas, x, round(a * x + b))
    else:
        # A steep line climbs more than one row per column, so stepping through x
        # leaves gaps. Step through y instead, and find x for each row.
        y_first = round(a * start_x + b)
        y_last = round(a * end_x + b)
        for y in range(min(y_first, y_last), max(y_first, y_last) + 1):
            paint_xy(canvas, round((y - b) / a), y)
