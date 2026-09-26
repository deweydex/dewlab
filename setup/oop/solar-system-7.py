class Probe:
    """One space probe: a name, and fuel in kilograms, from 0 up to
    tank_size."""

    tank_size = 100

    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel

    def __str__(self):
        return f"{self.name} (fuel {self._fuel} kg)"

    def get_fuel(self):
        """Return the probe's fuel in kilograms."""
        return self._fuel

    def can_burn(self, kg):
        """Return True if the probe can burn kg kilograms now.

        >>> Probe("Voyager", 70).can_burn(30)
        True
        >>> Probe("Voyager", 70).can_burn(80)
        False
        >>> Probe("Voyager", 70).can_burn(-5)
        False
        """
        if kg < 0:
            return False
        return kg <= self._fuel

    def burn(self, kg):
        """Burn kg kilograms of fuel.

        kg: a number of kilograms, 0 or more.
        Refuses, prints why, and changes nothing if can_burn(kg) is False.
        Returns nothing.
        """
        if not self.can_burn(kg):
            print(f"Refused: {self.name} cannot burn {kg} kg now.")
            return
        self._fuel = self._fuel - kg

    def refuel(self, kg):
        """Add kg kilograms of fuel, stopping at tank_size.

        kg: a number of kilograms, 0 or more. Returns nothing.
        """
        self._fuel = min(self.tank_size, self._fuel + kg)


class Lander(Probe):
    """A probe that can land. Once it has landed, it burns no more fuel."""

    def __init__(self, name, fuel):
        super().__init__(name, fuel)
        self._landed = False

    def land(self):
        """Land the probe. Returns nothing."""
        self._landed = True

    def can_burn(self, kg):
        """Return False once the lander has landed; before that, answer as
        any probe would."""
        if self._landed:
            return False
        return super().can_burn(kg)


class Mission:
    """A mission, and the probes it has launched."""

    def __init__(self, name):
        self.name = name
        self._probes = []

    def launch(self, probe):
        """Add probe to the mission. Returns nothing."""
        self._probes.append(probe)

    def total_fuel(self):
        """Return the fuel of every probe in the mission, added up, in
        kilograms."""
        total = 0
        for probe in self._probes:
            total = total + probe.get_fuel()
        return total

    def ready_for(self, kg):
        """Return a list of the names of the probes that can burn kg
        kilograms now."""
        names = []
        for probe in self._probes:
            if probe.can_burn(kg):
                names.append(probe.name)
        return names
