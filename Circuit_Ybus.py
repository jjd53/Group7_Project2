import numpy as np
import pandas as pd
from Bus import Bus
from Transformer_PUS import Transformer
from TransmissionLine_PUS import TransmissionLine
from Conductor import Conductor
from Bundle import Bundle
from Geometry import Geometry


class Circuit_Ybus:
    def __init__(self, name: str):
        """ Initializes the Circuit object with dictionaries to store components """
        self.name = name
        self.buses = {}
        self.transformers = {}
        self.conductors = {}
        self.tlines = {}
        self.bundles = {}
        self.geometries = {}
        self.ybus = None  # Will be computed later
        self.calc_ybus()


    def add_bus(self, name, base_kv):
        """ Adds a Bus object to the circuit """
        self.buses[name] = Bus(name, base_kv)


    def add_conductor(self, name, diam, GMR, resistance, ampacity):
        """ Adds a Conductor object to the circuit """
        self.conductors[name] = Conductor(name, diam, GMR, resistance, ampacity)


    def add_bundle(self, name, num_conductors, spacing, conductor):
        """ Adds a Bundle object using an existing conductor """
        if conductor in self.conductors:
            self.bundles[name] = Bundle(name, num_conductors, spacing, self.conductors[conductor])
        else:
            raise ValueError(f"Conductor '{conductor}' not found in the circuit.")


    def add_geometry(self, name, xa, ya, xb, yb, xc, yc):
        """ Adds a Geometry object to the circuit """
        self.geometries[name] = Geometry(name, xa, ya, xb, yb, xc, yc)


    def add_transformer(self, name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio, V1, V2):
        """ Adds a Transformer object between two buses """
        if bus1 in self.buses and bus2 in self.buses:
            self.transformers[name] = Transformer(name, self.buses[bus1], self.buses[bus2], power_rating, impedance_percent, x_over_r_ratio, V1, V2)
        else:
            raise ValueError(f"One or both buses '{bus1}', '{bus2}' not found in the circuit.")


    def add_tline(self, name: str, bus1: str, bus2: str, bundle, geometry, length: float, frequency=60):
        """ Adds a Transmission Line object between two buses """
        if bus1 in self.buses and bus2 in self.buses and bundle in self.bundles and geometry in self.geometries:
            self.tlines[name] = TransmissionLine(name, self.buses[bus1], self.buses[bus2], self.bundles[bundle], self.geometries[geometry], length, frequency)
        else:
            raise ValueError(f"One or more components for Transmission Line '{name}' not found in the circuit.")

    # Compute Ybus Matrix
    def calc_ybus(self):
        """ Constructs the Ybus matrix by summing Yprim matrices of transformers and transmission lines """
        num_buses = len(self.buses)
        bus_names = list(self.buses.keys())

        # Initialize an empty Ybus matrix
        Ybus_matrix = np.zeros((num_buses, num_buses), dtype=complex)

        # Process transformers
        for transformer in self.transformers.values():
            yprim = transformer.YPrim_matrix.values
            i = bus_names.index(transformer.bus1.name)
            j = bus_names.index(transformer.bus2.name)

            # Add admittances to Ybus
            Ybus_matrix[i, i] += yprim[0, 0]
            Ybus_matrix[i, j] += yprim[0, 1]
            Ybus_matrix[j, i] += yprim[1, 0]
            Ybus_matrix[j, j] += yprim[1, 1]

        # Process transmission lines
        for line in self.tlines.values():
            yprim = line.YPrim_matrix.values
            i = bus_names.index(line.bus1.name)
            j = bus_names.index(line.bus2.name)

            # Add admittances to Ybus
            Ybus_matrix[i, i] += yprim[0, 0]
            Ybus_matrix[i, j] += yprim[0, 1]
            Ybus_matrix[j, i] += yprim[1, 0]
            Ybus_matrix[j, j] += yprim[1, 1]

        # Store final Ybus matrix
        self.ybus = pd.DataFrame(Ybus_matrix, index=bus_names, columns=bus_names)
