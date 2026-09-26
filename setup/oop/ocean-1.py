class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def __str__(self):
        return f"{self.name} at {self.depth} m"

    def dive(self, metres):
        self.depth = self.depth + metres

    def rise(self, metres):
        self.depth = max(0, self.depth - metres)
