def show_picture(canvas, darkest=1):
    """Draw a canvas. A square with 0 ink is white. A square with `darkest` ink or more is black."""
    import matplotlib.pyplot as plt

    rows = len(canvas)
    columns = len(canvas[0])
    longest = max(rows, columns)
    size = min(7, max(3, longest / 5))
    plt.figure(figsize=(size * columns / longest, size * rows / longest))
    plt.imshow(canvas, cmap="gray_r", vmin=0, vmax=darkest, interpolation="nearest")
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


def paint_rectangle(canvas, top, left, bottom, right):
    for row in range(top, bottom + 1):
        paint_horizontal(canvas, row, left, right)


def paint_square(canvas, top, left, size):
    paint_rectangle(canvas, top, left, top + size - 1, left + size - 1)


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


def paint_gradient(canvas, top, left, bottom, right):
    height = bottom - top + 1
    for step in range(height):
        for column in range(left, right + 1):
            canvas[top + step][column] = canvas[top + step][column] + (height - step)


def paint_xy(canvas, x, y):
    """Paint the cell at (x, y). The origin (0, 0) is the bottom-left cell."""
    row = len(canvas) - 1 - y
    if 0 <= row < len(canvas) and 0 <= x < len(canvas[0]):
        paint_point(canvas, row, x)


def paint_line(canvas, a, b, start_x, end_x):
    if abs(a) <= 1:
        for x in range(start_x, end_x + 1):
            paint_xy(canvas, x, round(a * x + b))
    else:
        y_first = round(a * start_x + b)
        y_last = round(a * end_x + b)
        for y in range(min(y_first, y_last), max(y_first, y_last) + 1):
            paint_xy(canvas, round((y - b) / a), y)
