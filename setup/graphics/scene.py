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


def with_ones(points):
    """Three rows of x, y and z, with a fourth row of ones."""
    return points + [[1] * len(points[0])]


def translation(dx, dy, dz):
    return [[1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]]


def rotation_x(angle):
    c, s = math.cos(angle), math.sin(angle)
    return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]


def rotation_y(angle):
    c, s = math.cos(angle), math.sin(angle)
    return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]


def rotation_z(angle):
    c, s = math.cos(angle), math.sin(angle)
    return [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def scaling(k):
    return [[k, 0, 0, 0], [0, k, 0, 0], [0, 0, k, 0], [0, 0, 0, 1]]


def projection(fov_degrees, near=0.1, far=100):
    f = 1 / math.tan(math.radians(fov_degrees) / 2)
    return [[f, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (far - near), -2 * far * near / (far - near)],
            [0, 0, 1, 0]]


def chain(*matrices):
    """One 4x4 matrix that does every matrix given. The last one acts first."""
    result = matrices[0]
    for matrix in matrices[1:]:
        result = multiply(result, matrix)
    return result


def place(shape, matrix):
    """A copy of shape, a (points, edges) pair, moved by a 4x4 matrix."""
    points, edges = shape
    return multiply(matrix, with_ones(points))[:3], edges


def combine(shapes):
    """One (points, edges) pair holding every shape in the list."""
    xs, ys, zs, all_edges = [], [], [], []
    for points, edges in shapes:
        offset = len(xs)
        xs = xs + list(points[0])
        ys = ys + list(points[1])
        zs = zs + list(points[2])
        all_edges = all_edges + [(start + offset, end + offset) for start, end in edges]
    return [xs, ys, zs], all_edges


def draw_wireframe(shape, camera, color="C0", near=0.1):
    """Draw a (points, edges) pair through a 4x4 camera matrix.

    An edge with either end nearer than `near` is left out, so nothing is
    ever divided by a depth of 0 or less.
    """
    points, edges = shape
    xs, ys, zs, ws = multiply(camera, with_ones(points))
    for start, end in edges:
        if ws[start] < near or ws[end] < near:
            continue
        plt.plot([xs[start] / ws[start], xs[end] / ws[end]],
                 [ys[start] / ws[start], ys[end] / ws[end]], color=color)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.gca().set_aspect("equal")
