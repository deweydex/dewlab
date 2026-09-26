class Submarine:
    def __init__(self, name):
        self.name = name
        self._depth = 0

    def __str__(self):
        return f"{self.name} at {self._depth} m"

    def get_depth(self):
        return self._depth

    def dive(self, metres):
        if self._depth + metres > 400:
            print("Refused: the hull is safe only to 400 m.")
            return
        self._depth = self._depth + metres

    def rise(self, metres):
        self._depth = max(0, self._depth - metres)
