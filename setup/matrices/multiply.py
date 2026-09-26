def transpose(m):
    """A new matrix: the rows of m become its columns."""
    return [[row[j] for row in m] for j in range(len(m[0]))]


def dot(a, b):
    """The dot product: each pair multiplied, then added up."""
    if len(a) != len(b):
        raise ValueError("lengths do not match")
    return sum(x * y for x, y in zip(a, b))


def multiply(a, b):
    """The matrix product ab: row i of a with column j of b, in every place."""
    columns = transpose(b)
    return [[dot(row, column) for column in columns] for row in a]
