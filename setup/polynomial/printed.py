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

    def __str__(self):
        text = ""
        for power in range(self.degree(), -1, -1):
            coefficient = self._coefficients[power]
            if coefficient != 0:
                if coefficient < 0 and text == "":
                    text = "-"
                elif coefficient < 0:
                    text = text + " - "
                elif text != "":
                    text = text + " + "
                size = abs(coefficient)
                if size != 1 or power == 0:
                    text = text + str(size)
                if power == 1:
                    text = text + "x"
                elif power > 1:
                    text = text + "x^" + str(power)
        if text == "":
            return "0"
        return text
