def make_set(items):
    """Return a sorted list of the different items, with no repeats."""
    result = []
    for item in sorted(items):
        if len(result) == 0 or item != result[-1]:
            result.append(item)
    return result


def union(a, b):
    """Return a sorted list of the elements in a or b, or both."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            result.append(a[i])
            i = i + 1
        else:
            result.append(b[j])
            j = j + 1
    return result + a[i:] + b[j:]


def intersection(a, b):
    """Return a sorted list of the elements in both a and b."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            i = i + 1
        else:
            j = j + 1
    return result


def difference(a, b):
    """Return a sorted list of the elements in a that are not in b."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i = i + 1
            j = j + 1
        elif a[i] < b[j]:
            result.append(a[i])
            i = i + 1
        else:
            j = j + 1
    return result + a[i:]


def is_subset(a, b):
    """Return True if every element of a is also in b."""
    return intersection(a, b) == a
