def mean(data):
    """The mean: add up the values, and share the total out equally."""
    return sum(data) / len(data)


def median(data):
    """The middle value once the data is sorted."""
    ordered = sorted(data)
    n = len(ordered)
    middle = n // 2
    if n % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def mode(data):
    """The value that appears most often. On a tie, the one seen first."""
    counts = {}
    for value in data:
        if value not in counts:
            counts[value] = 0
        counts[value] = counts[value] + 1
    best = data[0]
    for value in counts:
        if counts[value] > counts[best]:
            best = value
    return best


def std_dev(data):
    """How far the values are from their mean, in a typical case."""
    centre = mean(data)
    total = 0
    for value in data:
        total = total + (value - centre) ** 2
    return (total / len(data)) ** 0.5
