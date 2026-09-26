class Character:
    """One character in the game: a name, and health from 0 up to
    max_health. A character with 0 health is down."""

    max_health = 10

    def __init__(self, name, health):
        self.name = name
        self._health = health

    def __str__(self):
        return f"{self.name} (health {self._health})"

    def get_health(self):
        """Return the character's health, a whole number."""
        return self._health

    def is_down(self):
        """Return True if the character's health is 0.

        >>> Character("Ada", 0).is_down()
        True
        """
        return self._health == 0

    def take_damage(self, amount):
        """Take amount away from the character's health, stopping at 0.

        amount: a whole number, 0 or more.
        Refuses a negative amount, and prints why. Returns nothing.
        """
        if amount < 0:
            print("Refused: damage cannot be negative.")
            return
        self._health = max(0, self._health - amount)

    def heal(self, amount):
        """Add amount to the character's health, stopping at max_health.

        amount: a whole number, 0 or more.
        Refuses a negative amount, or a character who is down, and prints
        why. Returns nothing.
        """
        if amount < 0:
            print("Refused: healing cannot be negative.")
            return
        if self.is_down():
            print(f"Refused: {self.name} is down.")
            return
        self._health = min(self.max_health, self._health + amount)


class Healer(Character):
    """A character who can also heal someone else."""

    def heal_other(self, other, amount):
        """Ask other to heal by amount, by other's own rules.

        other: any character. amount: a whole number, 0 or more.
        Refuses if the healer is down, and prints why. Returns nothing.
        """
        if self.is_down():
            print(f"Refused: {self.name} is down.")
            return
        other.heal(amount)


class Room:
    """A room in the game, and the characters inside it. Nobody is inside
    twice."""

    def __init__(self, name):
        self.name = name
        self._characters = []

    def __str__(self):
        return f"{self.name}: {len(self.standing())} standing"

    def enter(self, character):
        """Put character in the room.

        Refuses a character who is already inside, and prints why.
        Returns nothing.
        """
        if character in self._characters:
            print(f"Refused: {character.name} is already in {self.name}.")
            return
        self._characters.append(character)

    def standing(self):
        """Return a list of the names of the characters who are not down.

        >>> cave = Room("Cave")
        >>> cave.enter(Character("Ada", 10))
        >>> cave.standing()
        ['Ada']
        """
        names = []
        for character in self._characters:
            if not character.is_down():
                names.append(character.name)
        return names
