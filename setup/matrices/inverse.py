def det(m):
    """The determinant of the 2x2 matrix m: ad - bc."""
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def inverse(m):
    """The matrix that undoes the 2x2 matrix m."""
    d = det(m)
    if d == 0:
        raise ValueError("this matrix has determinant 0, so it cannot be undone")
    return [[m[1][1] / d, -m[0][1] / d], [-m[1][0] / d, m[0][0] / d]]
