import math
import random


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


def paint_segment(canvas, x1, y1, x2, y2):
    if x1 == x2:
        # A vertical line has no slope, so walk up it one square at a time.
        for y in range(min(y1, y2), max(y1, y2) + 1):
            paint_xy(canvas, x1, y)
    else:
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        paint_line(canvas, a, b, min(x1, x2), max(x1, x2))


def paint_starburst(canvas, x, y, spacing):
    rows = len(canvas)
    columns = len(canvas[0])
    for column in range(0, columns, spacing):
        paint_segment(canvas, x, y, column, 0)
        paint_segment(canvas, x, y, column, rows - 1)
    for row in range(0, rows, spacing):
        paint_segment(canvas, x, y, 0, row)
        paint_segment(canvas, x, y, columns - 1, row)


def paint_fan(canvas, corner, first_end, second_end, steps):
    corner_x, corner_y = corner
    first_x, first_y = first_end
    second_x, second_y = second_end
    for step in range(steps + 1):
        fraction = step / steps
        # One end of the string slides in from first_end to the corner,
        # and the other end slides out from the corner to second_end.
        x1 = round(first_x + (corner_x - first_x) * fraction)
        y1 = round(first_y + (corner_y - first_y) * fraction)
        x2 = round(corner_x + (second_x - corner_x) * fraction)
        y2 = round(corner_y + (second_y - corner_y) * fraction)
        paint_segment(canvas, x1, y1, x2, y2)


def polygon_points(center_x, center_y, radius, sides):
    points = []
    for corner in range(sides):
        angle = 2 * math.pi * corner / sides
        x = round(center_x + radius * math.cos(angle))
        y = round(center_y + radius * math.sin(angle))
        points.append((x, y))
    return points


def paint_polygon(canvas, points):
    for index in range(len(points)):
        x1, y1 = points[index]
        x2, y2 = points[(index + 1) % len(points)]   # the % joins the last point back to the first
        paint_segment(canvas, x1, y1, x2, y2)


def paint_star(canvas, points, step):
    for index in range(len(points)):
        x1, y1 = points[index]
        x2, y2 = points[(index + step) % len(points)]
        paint_segment(canvas, x1, y1, x2, y2)


def paint_where(canvas, rule):
    for row in range(len(canvas)):
        for column in range(len(canvas[0])):
            ink = rule(column, row)      # x is the column and y is the row
            canvas[row][column] = canvas[row][column] + ink


def paint_floor(canvas, horizon, vanishing_x, spacing):
    columns = len(canvas[0])
    for x in range(0, columns, spacing):
        # Lines that run away from us all point at the vanishing point.
        paint_segment(canvas, x, 0, vanishing_x, horizon)
    for distance in range(4, 40):
        # Equal steps in distance land closer and closer together on the picture.
        y = horizon - round(400 / distance)
        paint_horizontal(canvas, y, 0, columns - 1)


def dot(first, second):
    total = 0
    for index in range(len(first)):
        total = total + first[index] * second[index]
    return total


def get_patch(canvas, row, column, size):
    patch = []
    for r in range(row, row + size):
        patch.append(canvas[r][column:column + size])    # a slice takes size numbers from one row
    return patch


def flatten(grid):
    flat = []
    for row in grid:
        for value in row:
            flat.append(value)
    return flat


def apply_kernel(canvas, kernel, row, column):
    patch = get_patch(canvas, row, column, len(kernel))
    return dot(flatten(patch), flatten(kernel))


def convolve(canvas, kernel):
    size = len(kernel)
    result = make_canvas(len(canvas) - size + 1, len(canvas[0]) - size + 1)
    for row in range(len(result)):
        for column in range(len(result[0])):
            result[row][column] = apply_kernel(canvas, kernel, row, column)
    return result


def absolute(canvas):
    result = make_canvas(len(canvas), len(canvas[0]))
    for row in range(len(canvas)):
        for column in range(len(canvas[0])):
            result[row][column] = abs(canvas[row][column])
    return result


def cube_picture():
    """A cube on a table in perspective. Edges hold 3 ink, so show it with darkest=3."""
    canvas = make_canvas(120, 120)

    for row in range(28, 41):                    # the shadow on the table, to the right of the cube
        left = round(60 + (row - 28) / 3)
        paint_horizontal(canvas, row, left, left + 16)
    paint_rectangle(canvas, 28, 30, 58, 60)      # the front face
    for x in range(60, 65):                      # the shaded side, one column at a time
        for layer in range(2):
            paint_vertical(canvas, x, round(3 * x - 152), round(1.5 * x - 32))

    for layer in range(3):
        paint_horizontal(canvas, 14, 6, 100)     # the table: front edge and back edge
        paint_horizontal(canvas, 51, 65, 90)     # the cube hides the rest of the back edge
        paint_line(canvas, 1, 8, 6, 29)          # its two sides run towards the vanishing point
        paint_line(canvas, -3.7, 384, 90, 100)   # the cube hides the left side from x = 30
        paint_horizontal(canvas, 6, 6, 100)      # the table's edge, and its legs
        paint_vertical(canvas, 6, 6, 14)
        paint_vertical(canvas, 100, 6, 14)
        paint_rectangle(canvas, 0, 8, 5, 10)
        paint_rectangle(canvas, 0, 96, 5, 98)
        paint_horizontal(canvas, 28, 30, 60)     # the front face of the cube
        paint_horizontal(canvas, 58, 30, 60)
        paint_vertical(canvas, 30, 28, 58)
        paint_vertical(canvas, 60, 28, 58)
        paint_horizontal(canvas, 64, 40, 64)     # the back edges, seen above and beside it
        paint_vertical(canvas, 64, 40, 64)
        paint_line(canvas, 0.6, 40, 30, 40)      # three edges that run back to the vanishing point
        paint_line(canvas, 1.5, -32, 60, 64)
        paint_line(canvas, 3, -152, 60, 64)
    return canvas


def paint_random_points(canvas, count, seed):
    random.seed(seed)       # the same seed gives the same points every time
    for dot in range(count):
        row = random.randint(0, len(canvas) - 1)          # randint includes both ends
        column = random.randint(0, len(canvas[0]) - 1)
        paint_point(canvas, row, column)


def add_noise(canvas, chance, seed):
    random.seed(seed)
    for row in range(len(canvas)):
        for column in range(len(canvas[0])):
            if random.random() < chance:           # true about chance of the time
                canvas[row][column] = canvas[row][column] + 1


def paint_city(canvas, seed):
    random.seed(seed)       # the same seed gives the same city every time
    columns = len(canvas[0])
    paint_gradient(canvas, 80, 0, 99, columns - 1)
    for tallest in [45, 65]:                    # far buildings first, then near ones on top
        left = 0
        while left < columns:
            width = random.randint(8, 20)
            height = random.randint(20, tallest)
            right = min(left + width - 1, columns - 1)
            for layer in range(6):
                paint_rectangle(canvas, 0, left, height - 1, right)
            left = left + width + random.randint(0, 3)
    for layer in range(20):
        paint_rectangle(canvas, 0, 0, 9, columns - 1)       # the road
    for row in range(14, 60, 8):
        for column in range(2, columns - 4, 7):
            on_a_building = canvas[row][column] >= 6      # the sky has less than 6 ink here
            if on_a_building and random.random() < 0.3:    # about 3 windows in 10 are lit
                for layer in range(14):
                    paint_square(canvas, row, column, 3)


def random_walk(canvas, steps, seed):
    random.seed(seed)
    row = len(canvas) // 2
    column = len(canvas[0]) // 2
    for step in range(steps):
        paint_point(canvas, row, column)
        direction = random.randint(0, 3)
        if direction == 0:
            row = row + 1
        elif direction == 1:
            row = row - 1
        elif direction == 2:
            column = column + 1
        else:
            column = column - 1
        row = min(max(row, 0), len(canvas) - 1)             # stay on the canvas
        column = min(max(column, 0), len(canvas[0]) - 1)


def estimate_pi(darts, seed):
    random.seed(seed)
    inside = 0
    for dart in range(darts):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:                 # inside the quarter circle of radius 1
            inside = inside + 1
    return 4 * inside / darts                   # the quarter circle covers pi / 4 of the square


def chaos_game(canvas, corners, steps, seed):
    random.seed(seed)
    x, y = corners[0]
    for step in range(steps):
        corner_x, corner_y = random.choice(corners)
        x = (x + corner_x) / 2                  # move halfway towards a corner
        y = (y + corner_y) / 2
        paint_xy(canvas, round(x), round(y))


def dither(canvas, darkest, seed):
    random.seed(seed)
    result = make_canvas(len(canvas), len(canvas[0]))
    for row in range(len(canvas)):
        for column in range(len(canvas[0])):
            chance = canvas[row][column] / darkest
            if random.random() < chance:
                result[row][column] = 1
    return result


def combine(first, second):
    result = make_canvas(len(first), len(first[0]))
    for row in range(len(first)):
        for column in range(len(first[0])):
            a = first[row][column]
            b = second[row][column]
            result[row][column] = math.sqrt(a * a + b * b)     # the length of the pair (a, b)
    return result


def threshold(canvas, level):
    result = make_canvas(len(canvas), len(canvas[0]))
    for row in range(len(canvas)):
        for column in range(len(canvas[0])):
            if canvas[row][column] >= level:
                result[row][column] = 1
    return result


def score(first, second):
    total = 0
    for row in range(len(first)):
        for column in range(len(first[0])):
            difference = first[row][column] - second[row][column]
            total = total + difference * difference
    return total / (len(first) * len(first[0]))        # the average squared difference


def random_kernel(size, seed):
    random.seed(seed)
    kernel = []
    for row in range(size):
        kernel.append([random.uniform(-1, 1) for column in range(size)])    # uniform gives a decimal in a range
    return kernel


def best_of_random(canvas, target, tries, seed):
    best_kernel = random_kernel(3, seed)
    best_score = score(convolve(canvas, best_kernel), target)
    for attempt in range(1, tries):
        kernel = random_kernel(3, seed + attempt)
        kernel_score = score(convolve(canvas, kernel), target)
        if kernel_score < best_score:
            best_kernel = kernel
            best_score = kernel_score
    return best_kernel, best_score


def nudge_kernel(canvas, target, kernel, amount):
    new_kernel = [row[:] for row in kernel]              # a copy, so the old kernel stays as it was
    for row in range(len(kernel)):
        for column in range(len(kernel)):
            original = new_kernel[row][column]
            best_value = original
            best_score = score(convolve(canvas, new_kernel), target)
            for candidate in [original + amount, original - amount]:
                new_kernel[row][column] = candidate
                candidate_score = score(convolve(canvas, new_kernel), target)
                if candidate_score < best_score:
                    best_value = candidate
                    best_score = candidate_score
            new_kernel[row][column] = best_value          # keep whichever of the three was best
    return new_kernel


def kernel_gradient(canvas, target, kernel):
    size = len(kernel)
    output = convolve(canvas, kernel)
    count = len(output) * len(output[0])
    gradient = [[0] * size for row in range(size)]
    for row in range(len(output)):
        for column in range(len(output[0])):
            error = output[row][column] - target[row][column]
            for i in range(size):
                for j in range(size):
                    gradient[i][j] = gradient[i][j] + 2 * error * canvas[row + i][column + j] / count
    return gradient


def train_kernel(canvas, target, size, rounds, rate):
    kernel = [[0] * size for row in range(size)]
    scores = []
    for round_number in range(rounds):
        gradient = kernel_gradient(canvas, target, kernel)
        for i in range(size):
            for j in range(size):
                kernel[i][j] = kernel[i][j] - rate * gradient[i][j]
        scores.append(score(convolve(canvas, kernel), target))
    return kernel, scores
