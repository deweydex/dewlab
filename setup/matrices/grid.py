RAMP = " .:-=+*#%@"


def show(grid):
    """Draw a grid of numbers from 0 to 9 as text, one character a number."""
    for row in grid:
        line = ""
        for value in row:
            level = min(9, max(0, round(value)))
            line = line + RAMP[level]
        print(line)


def scale(k, m):
    """A new matrix: every entry of m multiplied by k."""
    return [[k * value for value in row] for row in m]


def add(a, b):
    """A new matrix: a and b added position by position."""
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("a and b are not the same shape")
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def transpose(m):
    """A new matrix: the rows of m become its columns."""
    return [[row[j] for row in m] for j in range(len(m[0]))]
