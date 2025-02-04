# Transformer.py
class Transformer:
    def __init__(self, name: str, bus1: str, bus2: str, power_rating: float, impedance_percent: float, x_over_r_ratio: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio

        # Impedance and admittance calculations
        self.zt = self.calc_impedance()
        self.yt = self.calc_admittance()
        self.yprim = None  

    def calc_impedance(self):
        # Calculate impedance in ohms using base impedance and percentage impedance
        base_impedance = (self.bus1.base_kv ** 2) / self.power_rating
        return (self.impedance_percent / 100) * base_impedance

    def calc_admittance(self):
        return 1 / self.zt if self.zt != 0 else float('inf')
