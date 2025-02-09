from Bus import Bus
from Conductor import Conductor
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Bundle import Bundle
from Geometry import Geometry

class Circuit:

    def __init__(self,name:str):
        self.name = name
        self.buses = {}
        self.transformers = {}
        self.conductors = {}
        self.tlines = {}
        self.bundles = {}
        self.geometries = {}



    def add_bus(self,bus,base_kv):
        self.buses[bus]=Bus(bus,base_kv)

    def add_conductor(self, name, diam, GMR, resistance, ampacity):
        self.conductors[name] = Conductor(name, diam, GMR, resistance, ampacity)

    def add_transformer(self, name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio):
        self.transformers[name] = Transformer(name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio)

    def add_tline(self, name: str, bus1: Bus, bus2: Bus, bundle, geometry, length: float, frequency=60):
        self.tlines[name] = TransmissionLine(name, bus1, bus2, bundle, geometry, length, frequency)

    def add_bundle(self, name, num_conductors, spacing, conductor):
        self.bundles[name]=Bundle(name, num_conductors, spacing, conductor)

    def add_geometry(self, name, xa, ya, xb, yb, xc, yc):
        self.geometries[name]=Geometry(name, xa, ya, xb, yb, xc, yc)

