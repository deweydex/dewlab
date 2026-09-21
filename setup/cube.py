import math
import matplotlib.pyplot as plt

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]

def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]

cube = [
    [-1, 1, 1, -1, -1, 1, 1, -1],   # x of each corner
    [-1, -1, 1, 1, -1, -1, 1, 1],   # y
    [-1, -1, -1, -1, 1, 1, 1, 1],   # z
]
edges = [(0, 1), (1, 2), (2, 3), (3, 0),
         (4, 5), (5, 6), (6, 7), (7, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]

def move(points, dx, dy, dz):
    xs, ys, zs = points
    return [[x + dx for x in xs], [y + dy for y in ys], [z + dz for z in zs]]

def project(points):
    xs, ys, zs = points
    return [[x / z for x, z in zip(xs, zs)], [y / z for y, z in zip(ys, zs)]]

def draw_edges(screen_points, color="C0", limit=0.6):
    screen_xs, screen_ys = screen_points
    for start, end in edges:
        plt.plot([screen_xs[start], screen_xs[end]],
                 [screen_ys[start], screen_ys[end]], color=color)
    plt.xlim(-limit, limit)
    plt.ylim(-limit, limit)
    plt.gca().set_aspect("equal")

def draw(points, color="C0"):
    draw_edges(project(points), color)

def rotate_y(angle):
    cos_angle, sin_angle = math.cos(angle), math.sin(angle)
    return [[cos_angle, 0, sin_angle],
            [0, 1, 0],
            [-sin_angle, 0, cos_angle]]

def rotate_x(angle):
    cos_angle, sin_angle = math.cos(angle), math.sin(angle)
    return [[1, 0, 0],
            [0, cos_angle, -sin_angle],
            [0, sin_angle, cos_angle]]
