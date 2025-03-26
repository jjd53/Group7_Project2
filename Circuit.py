from Bus import Bus
from Conductor import Conductor
from Transformer_PUS import Transformer
from TransmissionLine_PUS import TransmissionLine
from Generator import Generator
from Load import Load
from Bundle import Bundle
from Geometry import Geometry
from Settings import Settings
import numpy as np
import pandas as pd



class Circuit:

    def __init__(self,name:str):
        self.name = name
        self.buses = {}
        self.transformers = {}
        self.conductors = {}
        self.tlines = {}
        self.bundles = {}
        self.geometries = {}
        self.generators = {}
        self.loads = {}

    s=Settings()

    def add_bus(self,bus,base_kv,bus_type:str, vpu = 1.0,delta = 0.0):
        self.buses[bus]=Bus(bus,base_kv, bus_type, vpu, delta)

    def add_conductor(self, name, diam, GMR, resistance, ampacity):
        self.conductors[name] = Conductor(name, diam, GMR, resistance, ampacity)

    def add_transformer(self, name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio):
        self.transformers[name] = Transformer(name, self.buses[bus1], self.buses[bus2], power_rating, impedance_percent, x_over_r_ratio)

    def add_tline(self, name: str, bus1: str, bus2: str, bundle, geometry, length: float, frequency=60):
        self.tlines[name] = TransmissionLine(name, bus1, bus2, self.bundles[bundle], self.geometries[geometry], length, frequency)

    def add_bundle(self, name, num_conductors, spacing, conductor):
        self.bundles[name]=Bundle(name, num_conductors, spacing, self.conductors[conductor])

    def add_geometry(self, name, xa, ya, xb, yb, xc, yc):
        self.geometries[name]=Geometry(name, xa, ya, xb, yb, xc, yc)

    def add_generator(self, name, bus, voltage_setpoint, mw_setpoint):
        self.generators[name] = Generator(name, bus, voltage_setpoint, mw_setpoint)

    def add_load(self, name, bus, real_power, reactive_power):
        self.loads[name] = Load(name, bus, real_power, reactive_power)

    def calc_ybus(self):
        """ Constructs the Ybus matrix by summing Yprim matrices of transformers and transmission lines """
        num_buses = len(self.buses)
        bus_names = list(self.buses.keys())

        # Initialize an empty Ybus matrix
        Ybus_matrix = np.zeros((num_buses, num_buses), dtype=complex)

        # Process transformers
        for transformer in self.transformers.values():
            yprim = np.array(transformer.YPrim_matrix)
            i = bus_names.index(transformer.bus1.name)
            j = bus_names.index(transformer.bus2.name)

            # Add admittances to Ybus
            Ybus_matrix[i, i] += yprim[0, 0]
            Ybus_matrix[i, j] += yprim[0, 1]
            Ybus_matrix[j, i] += yprim[1, 0]
            Ybus_matrix[j, j] += yprim[1, 1]

        # Process transmission lines
        for line in self.tlines.values():
            yprim = np.array(line.YPrim_matrix)
            i = bus_names.index(line.bus1)
            j = bus_names.index(line.bus2)

            # Add admittances to Ybus
            Ybus_matrix[i, i] += yprim[0, 0]
            Ybus_matrix[i, j] += yprim[0, 1]
            Ybus_matrix[j, i] += yprim[1, 0]
            Ybus_matrix[j, j] += yprim[1, 1]

        # Store final Ybus matrix
        self.ybus = pd.DataFrame(Ybus_matrix, index=bus_names, columns=bus_names)
