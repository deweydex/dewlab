class Probe:
    tank_size = 100

    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel

    def __str__(self):
        return f"{self.name} (fuel {self._fuel} kg)"

    def get_fuel(self):
        return self._fuel

    def can_burn(self, kg):
        return kg <= self._fuel

    def burn(self, kg):
        if not self.can_burn(kg):
            print(f"Refused: {self.name} cannot burn {kg} kg now.")
            return
        self._fuel = self._fuel - kg

    def refuel(self, kg):
        self._fuel = min(self.tank_size, self._fuel + kg)
