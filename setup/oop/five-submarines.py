class SubmarineA:
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
        if metres >= self.room_below():
            print(f"Refused: the hull is safe only to {self.hull_limit} m.")
            return
        self._depth = self._depth + metres

    def rise(self, metres):
        self._depth = max(0, self._depth - metres)


class SubmarineB:
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
        self._depth = self._depth + metres
        if self._depth > self.hull_limit:
            print(f"Refused: the hull is safe only to {self.hull_limit} m.")
            return

    def rise(self, metres):
        self._depth = max(0, self._depth - metres)


class SubmarineC:
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


class SubmarineD:
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
        if metres > self.hull_limit:
            print(f"Refused: the hull is safe only to {self.hull_limit} m.")
            return
        self._depth = self._depth + metres

    def rise(self, metres):
        self._depth = max(0, self._depth - metres)


class SubmarineE:
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
        self._depth = self._depth - metres
