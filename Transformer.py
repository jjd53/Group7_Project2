# Transformer.py
from Bus import Bus
class Transformer:
    def __init__(self, name: str, bus1: Bus, bus2: Bus, power_rating: float, impedance_percent: float,
                 x_over_r_ratio: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio

        # Calculate impedance using provided formulas
        self.zt = self.calc_impedance()
        self.rt, self.xt = self.calc_rt_xt()  # Separate resistance and reactance
        self.yt = self.calc_admittance()
        self.yprim = None  # Placeholder for milestone 3

    def calc_impedance(self):
        # Base impedance calculation
        base_impedance = (self.bus1.base_kv ** 2) / self.power_rating
        return (self.impedance_percent / 100) * base_impedance

    def calc_rt_xt(self):
        # Calculate resistance and reactance using the X/R ratio
        rt = self.zt / ((1 + (self.x_over_r_ratio ** 2)) ** 0.5)
        xt = rt * self.x_over_r_ratio
        return rt, xt

    def calc_admittance(self):
        return 1 / self.zt if self.zt != 0 else float('inf')
