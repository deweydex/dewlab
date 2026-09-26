class Polynomial:
    def __init__(self, coefficients):
        coefficients = list(coefficients)
        while len(coefficients) > 1 and coefficients[-1] == 0:
            coefficients.pop()
        self._coefficients = coefficients

    def evaluate(self, x):
        total = 0
        for power in range(len(self._coefficients)):
            total = total + self._coefficients[power] * x ** power
        return total

    def degree(self):
        return len(self._coefficients) - 1
