import math
import pandas as pd


class TransmissionLine:
    def __init__(self, name: str, bus1, bus2, bundle, geometry, length: float, frequency=60):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length  # Length in miles
        self.frequency = frequency

        # Compute per-unit parameters
        self.Rpu, self.Xpu, self.Bpu = self.calc_impedance()
        self.Yseries = self.calc_admittance()

    def calc_impedance(self):
        """
        Converts impedance and admittance to per-unit values.
        """
        r_series = self.bundle.conductor.resistance / self.bundle.num_conductors  # Resistance per mile
        x_series = 2 * math.pi * self.frequency * 2e-7 * math.log(self.geometry.Deq / self.bundle.DSL) * 1609.34  # Reactance
        b_shunt = 2 * math.pi * self.frequency * (2 * math.pi * 8.854e-12) * math.log(self.geometry.Deq / self.bundle.DSC) * 1609.34  # Shunt Admittance

        # Convert to per-unit
        base_impedance = (self.bus1.base_kv ** 2) / 100  # Base Impedance using 100 MVA base
        Rpu = (r_series * self.length) / base_impedance
        Xpu = (x_series * self.length) / base_impedance
        Bpu = (b_shunt * self.length) * base_impedance  # Shunt Susceptance in per-unit
        return Rpu, Xpu, Bpu

    def calc_admittance(self):
        """
        Computes per-unit series admittance.
        """
        return 1 / complex(self.Rpu, self.Xpu) if self.Rpu or self.Xpu else float('inf')

    def calc_yprim(self):
        """
        Computes the primitive admittance matrix in per-unit.
        """
        Yprim_matrix = [[self.Yseries + (self.Bpu / 2), -self.Yseries], [-self.Yseries, self.Yseries + (self.Bpu / 2)]]
        self.YPrim_matrix = Yprim_matrix
        return pd.DataFrame(Yprim_matrix, index=[self.bus1.name, self.bus2.name], columns=[self.bus1.name, self.bus2.name])
