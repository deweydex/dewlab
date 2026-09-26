class Character:
    max_health = 10

    def __init__(self, name, health):
        self.name = name
        self._health = health

    def __str__(self):
        return f"{self.name} (health {self._health})"

    def get_health(self):
        return self._health

    def is_down(self):
        return self._health == 0

    def take_damage(self, amount):
        if amount < 0:
            print("Refused: damage cannot be negative.")
            return
        self._health = max(0, self._health - amount)

    def heal(self, amount):
        if amount < 0:
            print("Refused: healing cannot be negative.")
            return
        if self.is_down():
            print(f"Refused: {self.name} is down.")
            return
        self._health = min(self.max_health, self._health + amount)


class Healer(Character):
    # A healer is a character who can also heal someone else.

    def heal_other(self, other, amount):
        if self.is_down():
            print(f"Refused: {self.name} is down.")
            return
        other.heal(amount)


class Room:
    def __init__(self, name):
        self.name = name
        self._characters = []

    def __str__(self):
        return f"{self.name}: {len(self.standing())} standing"

    def enter(self, character):
        if character in self._characters:
            print(f"Refused: {character.name} is already in {self.name}.")
            return
        self._characters.append(character)

    def standing(self):
        names = []
        for character in self._characters:
            if not character.is_down():
                names.append(character.name)
        return names
