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


class Mission:
    def __init__(self, name):
        self.name = name
        self._probes = []

    def launch(self, probe):
        self._probes.append(probe)

    def total_fuel(self):
        total = 0
        for probe in self._probes:
            total = total + probe.get_fuel()
        return total

    def ready_for(self, kg):
        names = []
        for probe in self._probes:
            if probe.can_burn(kg):
                names.append(probe.name)
        return names
