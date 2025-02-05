# TransmissionLine.py
from Bus import Bus
class TransmissionLine:
    def __init__(self, name: str, bus1: Bus, bus2: Bus, bundle, geometry, length: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length

        # Line parameter calculations
        self.r_series, self.x_series, self.b_shunt = self.calc_line_parameters()
        self.zseries = self.r_series + 1j * self.x_series
        self.yshunt = 1j * self.b_shunt
        self.yprim = None  # Placeholder for milestone 3

    def calc_line_parameters(self):
        # Assuming the formulas are given in the reference materials
        resistance_per_km = self.bundle.conductor.resistance
        reactance_per_km = 0.1  # Placeholder; can be derived from geometry and inductance
        susceptance_per_km = 0.01  # Placeholder; can be derived from geometry and capacitance

        r_series = resistance_per_km * self.length
        x_series = reactance_per_km * self.length
        b_shunt = susceptance_per_km * self.length

        return r_series, x_series, b_shunt
