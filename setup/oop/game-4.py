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
        if self.is_down():
            print(f"Refused: {self.name} is down.")
            return
        self._health = min(self.max_health, self._health + amount)
