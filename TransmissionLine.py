# TransmissionLine.py
from Bus import Bus
import math
class TransmissionLine:
    def __init__(self, name: str, bus1: str, bus2: str, bundle, geometry, length: float, frequency=60):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length  # Length in miles
        self.frequency = frequency

        # Line parameter calculations
        self.r_series, self.x_series, self.b_shunt = self.calc_line_parameters()
        self.zseries = complex(self.r_series, self.x_series)
        self.yshunt = complex(0, self.b_shunt)
        self.yprim = self.calc_yprim()  # Calculate Y-prim matrix

    def calc_line_parameters(self):
        r_series = self.bundle.conductor.resistance / self.bundle.num_conductors  # Resistance per mile

        # Calculate reactance using provided formula
        x_series = 2 * math.pi * self.frequency * 2e-7 * math.log(self.geometry.Deq / self.bundle.DSL) * 1609.34

        # Calculate shunt susceptance using provided formula
        b_shunt = 2 * math.pi * self.frequency * (2 * math.pi * 8.854e-12) * math.log(
            self.geometry.Deq / self.bundle.DSC) * 1609.34

        # Scale values by the length of the transmission line
        return r_series * self.length, x_series * self.length, b_shunt * self.length

    def calc_yprim(self):
        y_series = 1 / self.zseries if self.zseries != 0 else complex('inf')
        y_shunt_half = self.yshunt / 2  # Half of shunt admittance on each end

        return [[y_series + y_shunt_half, -y_series], [-y_series, y_series + y_shunt_half]]
