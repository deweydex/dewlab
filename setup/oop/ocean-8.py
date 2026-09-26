class Submarine:
    """One submarine: a name and a depth in metres, from 0 at the surface
    down to hull_limit."""

    hull_limit = 400

    def __init__(self, name):
        self.name = name
        self._depth = 0

    def __str__(self):
        return f"{self.name} at {self._depth} m"

    def get_depth(self):
        """Return the submarine's depth in metres."""
        return self._depth

    def room_below(self):
        """Return how many metres the submarine can still dive.

        >>> Submarine("Nautilus").room_below()
        400
        """
        return self.hull_limit - self._depth

    def dive(self, metres):
        """Go metres deeper.

        metres: a whole number of metres.
        Refuses a dive past hull_limit, prints why, and changes nothing.
        Returns nothing.
        """
        if metres > self.room_below():
            print(f"Refused: the hull is safe only to {self.hull_limit} m.")
            return
        self._depth = self._depth + metres

    def rise(self, metres):
        """Come up by metres, stopping at the surface.

        metres: a whole number of metres, 0 or more.
        Refuses a negative number, and prints why. Returns nothing.
        """
        if metres < 0:
            print("Refused: rise needs a positive number of metres.")
            return
        self._depth = max(0, self._depth - metres)


class Bathyscaphe(Submarine):
    """A submarine built for the deepest trenches: its hull is safe to
    11,000 m.

    >>> Bathyscaphe("Trieste").room_below()
    11000
    """

    hull_limit = 11000


class Expedition:
    """An expedition, and the submarines it has."""

    def __init__(self, name):
        self.name = name
        self._submarines = []

    def add(self, submarine):
        """Add submarine to the expedition. Returns nothing."""
        self._submarines.append(submarine)

    def deepest(self):
        """Return the submarine that is deepest now.

        The expedition must have at least one submarine.
        """
        best = self._submarines[0]
        for submarine in self._submarines:
            if submarine.get_depth() > best.get_depth():
                best = submarine
        return best


def run_choice(submarine, choice):
    """Run one command for the submarine. Return False when the dive is over.

    choice: the command typed, as text: dive, rise, depth or quit. dive and
    rise move 50 m at a time. Any other text prints that it is not a
    command, and the dive goes on.
    """
    if choice == "dive":
        submarine.dive(50)
        print(submarine)
    elif choice == "rise":
        submarine.rise(50)
        print(submarine)
    elif choice == "depth":
        print(submarine, "with", submarine.room_below(), "m to spare")
    elif choice == "quit":
        return False
    else:
        print("Not a command:", choice)
    return True
