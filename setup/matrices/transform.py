import matplotlib.pyplot as plt


def transform(m, point):
    """Where the 2x2 matrix m sends the point (x, y)."""
    x, y = point
    return (m[0][0] * x + m[0][1] * y, m[1][0] * x + m[1][1] * y)


def transform_all(m, shape):
    """Every corner of shape, moved by m."""
    return [transform(m, point) for point in shape]


def draw_shapes(shapes, closed=True):
    """Draw each shape, a list of (x, y) points, on one pair of axes."""
    plt.figure()
    for shape in shapes:
        xs = [x for x, y in shape]
        ys = [y for x, y in shape]
        if closed:
            xs.append(xs[0])
            ys.append(ys[0])
        plt.plot(xs, ys, marker="o")
    plt.axhline(0, color="grey", linewidth=0.5)
    plt.axvline(0, color="grey", linewidth=0.5)
    plt.gca().set_aspect("equal")
