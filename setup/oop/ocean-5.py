class Submarine:
    hull_limit = 400

    def __init__(self, name):
        self.name = name
        self._depth = 0

    def __str__(self):
        return f"{self.name} at {self._depth} m"

    def get_depth(self):
        return self._depth

    def room_below(self):
        return self.hull_limit - self._depth

    def dive(self, metres):
        if metres > self.room_below():
            print(f"Refused: the hull is safe only to {self.hull_limit} m.")
            return
        self._depth = self._depth + metres

    def rise(self, metres):
        self._depth = max(0, self._depth - metres)


class Bathyscaphe(Submarine):
    # A bathyscaphe is a submarine built for the deepest trenches.
    hull_limit = 11000


class Expedition:
    def __init__(self, name):
        self.name = name
        self._submarines = []

    def add(self, submarine):
        self._submarines.append(submarine)

    def deepest(self):
        best = self._submarines[0]
        for submarine in self._submarines:
            if submarine.get_depth() > best.get_depth():
                best = submarine
        return best
