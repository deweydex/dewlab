def eliminate(M):
    """The augmented matrix M in row echelon form, as a new list of rows.

    M is not changed.
    """
    rows = [list(row) for row in M]
    n = len(rows)
    for col in range(n):
        pivot = col
        while pivot < n and rows[pivot][col] == 0:
            pivot = pivot + 1
        if pivot == n:
            continue
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(col + 1, n):
            factor = rows[r][col] / rows[col][col]
            rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    return rows


def back_substitute(E):
    """The unknowns of a system whose augmented matrix E is in row echelon form."""
    n = len(E)
    values = [0] * n
    for i in range(n - 1, -1, -1):
        if abs(E[i][i]) < 1e-12:
            raise ValueError("this system does not have exactly one solution")
        known = sum(E[i][j] * values[j] for j in range(i + 1, n))
        values[i] = (E[i][n] - known) / E[i][i]
    return values


def solve(M):
    """The solution of the system whose augmented matrix is M."""
    return back_substitute(eliminate(M))
