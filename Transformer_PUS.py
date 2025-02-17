import pandas as pd

class Transformer:
    def __init__(self, name: str, bus1, bus2, power_rating: float, impedance_percent: float, x_over_r_ratio: float):
        """
        Initializes the Transformer object with per-unit calculations.
        """
        self.name = name
        self.bus1 = bus1  # Bus on primary side
        self.bus2 = bus2  # Bus on secondary side
        self.power_rating = power_rating  # Transformer rated power in MVA
        self.impedance_percent = impedance_percent  # Transformer impedance in percentage
        self.x_over_r_ratio = x_over_r_ratio  # X/R ratio

        # Compute per-unit impedance FIRST before using them!
        self.Rpu, self.Xpu = self.calc_impedance()  # Compute Resistance and Reactance
        self.Yseries = self.calc_admittance()  # Compute Admittance
        self.Yprim = self.calc_yprim()  # Compute Y-Prim Matrix

    def calc_impedance(self):
        """
        Converts transformer impedance to per-unit values.
        """
        base_impedance = (self.bus1.base_kv ** 2) / self.power_rating  # Base Impedance in ohms
        Zpu = (self.impedance_percent / 100) * base_impedance  # Per-Unit Impedance
        Rpu = Zpu / ((1 + (self.x_over_r_ratio ** 2)) ** 0.5)  # Per-Unit Resistance
        Xpu = Rpu * self.x_over_r_ratio  # Per-Unit Reactance
        return Rpu, Xpu  # Returning both values correctly

    def calc_admittance(self):
        """
        Computes per-unit series admittance.
        """
        if self.Rpu == 0 and self.Xpu == 0:
            return complex('inf')  # Avoid division by zero
        return 1 / complex(self.Rpu, self.Xpu)

    def calc_yprim(self):
        """
        Computes the primitive admittance matrix in per-unit.
        """
        if self.Yseries == 0:
            return [[0, 0], [0, 0]]  # Prevent division errors

        Yprim_matrix = [[self.Yseries, -self.Yseries], [-self.Yseries, self.Yseries]]
        return pd.DataFrame(Yprim_matrix, index=[self.bus1.name, self.bus2.name], columns=[self.bus1.name, self.bus2.name])

    def display_transformer_info(self):
        """
        Prints transformer details for debugging and validation.
        """
        print(f"\n Transformer: {self.name}")
        print(f"   - Bus 1: {self.bus1.name} ({self.bus1.base_kv} kV)")
        print(f"   - Bus 2: {self.bus2.name} ({self.bus2.base_kv} kV)")
        print(f"   - Power Rating: {self.power_rating} MVA")
        print(f"   - Impedance: {self.impedance_percent}%")
        print(f"   - X/R Ratio: {self.x_over_r_ratio}")
        print(f"   - Rpu: {self.Rpu:.6f}, Xpu: {self.Xpu:.6f}")
        print(f"   - Yseries (per-unit): {self.Yseries:.6f}")
        print(f"   - Y-Prim Matrix:\n{self.calc_yprim()}")
