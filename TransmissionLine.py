# TransmissionLine.py
class TransmissionLine:
    def __init__(self, name: str, bus1: str, bus2: str, bundle, geometry, length: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length
        
        # Series impedance and admittance calculations
        self.zseries = self.calc_series_impedance()
        self.yshunt = self.calc_shunt_admittance()
        self.yprim = None 

    def calc_series_impedance(self):
        return self.length * self.bundle.conductor.resistance

    def calc_shunt_admittance(self):
        return 0.01 * self.length
