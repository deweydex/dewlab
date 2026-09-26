class Lander(Probe):
    # A lander is a probe that can land, and once down, it burns no more.

    def __init__(self, name, fuel):
        super().__init__(name, fuel)
        self._landed = False

    def land(self):
        self._landed = True

    def can_burn(self, kg):
        if self._landed:
            return False
        return super().can_burn(kg)
