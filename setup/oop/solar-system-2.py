class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel

    def __str__(self):
        return f"{self.name} (fuel {self._fuel} kg)"

    def get_fuel(self):
        return self._fuel

    def burn(self, kg):
        if kg > self._fuel:
            print("Refused: not enough fuel for that burn.")
            return
        self._fuel = self._fuel - kg

    def refuel(self, kg):
        self._fuel = self._fuel + kg
