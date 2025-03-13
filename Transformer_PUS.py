# Transformer.py
import pandas as pd
import numpy as np
from Bus import Bus

class Transformer:
    def __init__(self, name: str, bus1: Bus, bus2: Bus, power_rating: float, impedance_percent: float, x_over_r_ratio: float):
        """
        Initializes the Transformer object with per-unit calculations.
        """
        self.name = name
        self.bus1 = bus1  # Primary side bus
        self.bus2 = bus2  # Secondary side bus
        self.power_rating = power_rating  # Transformer rated power in MVA
        self.impedance_percent = impedance_percent  # Transformer impedance in percentage
        self.x_over_r_ratio = x_over_r_ratio  # X/R ratio

        # Compute per-unit impedance
        self.Rpu, self.Xpu = self.calc_impedance()  # Per-unit resistance & reactance
        self.Yseries = self.calc_admittance()  # Per-unit admittance
        self.Yprim = self.calc_yprim()  # DataFrame with Bus Labels

    def calc_impedance(self):
        """
        Converts transformer impedance to per-unit values.
        """
        # base_impedance = (self.bus1.base_kv ** 2) / self.power_rating  # Base Impedance in PU
        # Zpu = (self.impedance_percent / 100) * 100/self.power_rating  # Per-Unit Impedance
        # Rpu = Zpu / ((1 + (self.x_over_r_ratio ** 2)) ** 0.5)  # Per-Unit Resistance
        # Xpu = Rpu * self.x_over_r_ratio  # Per-Unit Reactance
        self.zt = self.impedance_percent / 100 * 100 / self.power_rating * np.exp(1j * np.arctan(self.x_over_r_ratio))
        Rpu = self.zt.real
        Xpu = self.zt.imag


        return Rpu, Xpu  # Returns both values

    def calc_admittance(self):
        """
        Computes per-unit series admittance.
        """
        if self.Rpu == 0 and self.Xpu == 0:
            return complex('inf')  # Avoid division by zero
        return 1 / complex(self.Rpu, self.Xpu)

    def calc_yprim(self):
        """
        Computes the per-unit primitive admittance matrix and returns a Pandas DataFrame.
        Now uses `self.Yseries` instead of recalculating `1 / self.Zpu`.
        """
        Yprim_matrix = [[self.Yseries, -self.Yseries], [-self.Yseries, self.Yseries]]  # Primitive admittance matrix
        self.YPrim_matrix = Yprim_matrix

        # Bus names as row and column labels
        bus_labels = [self.bus1.name, self.bus2.name]
        return pd.DataFrame(Yprim_matrix, index=bus_labels, columns=bus_labels)

    def display_transformer_info(self):
        """
        Prints transformer details for debugging and validation.
        """
        print(f"\n🔹 Transformer: {self.name}")
        print(f"   - Bus 1: {self.bus1.name} ({self.bus1.base_kv} kV)")
        print(f"   - Bus 2: {self.bus2.name} ({self.bus2.base_kv} kV)")
        print(f"   - Power Rating: {self.power_rating} MVA")
        print(f"   - Impedance: {self.impedance_percent}%")
        print(f"   - X/R Ratio: {self.x_over_r_ratio}")
        print(f"   - Rpu: {self.Rpu:.4f}, Xpu: {self.Xpu:.4f}")  # Rounded values
        print(f"   - Yseries (Per-Unit Admittance): {self.Yseries.real:.6f} + {self.Yseries.imag:.6f}j")
        print(f"   - Y-Prim Matrix:\n{self.Yprim.round(6)}")  # Prints DataFrame with bus labels
