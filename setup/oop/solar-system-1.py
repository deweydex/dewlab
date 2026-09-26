class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self.fuel = fuel

    def __str__(self):
        return f"{self.name} (fuel {self.fuel} kg)"

    def burn(self, kg):
        self.fuel = max(0, self.fuel - kg)

    def refuel(self, kg):
        self.fuel = self.fuel + kg
