class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def __str__(self):
        return f"{self.name} (health {self.health})"

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def heal(self, amount):
        self.health = self.health + amount
