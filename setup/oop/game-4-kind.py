class Healer(Character):
    # A healer is a character who can also heal someone else.

    def heal_other(self, other, amount):
        if self.is_down():
            print(f"Refused: {self.name} is down.")
            return
        other.heal(amount)
