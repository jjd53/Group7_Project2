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
        self.name = name
        self.buses = {}  
        self.transformers = {}  
        self.tlines = {} 
        self.conductors = {} 
        self.bundles = {}  
        self.geometries = {}
        self.ybus = None  

    # Add Bus
    def add_bus(self, name, base_kv):
        self.buses[name] = Bus(name, base_kv)

    # Add Conductor
    def add_conductor(self, name, diam, GMR, resistance, ampacity):
        self.conductors[name] = Conductor(name, diam, GMR, resistance, ampacity)

    # Add Transformer
    def add_transformer(self, name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio):
        if bus1 in self.buses and bus2 in self.buses:
            self.transformers[name] = Transformer(name, self.buses[bus1], self.buses[bus2], power_rating, impedance_percent, x_over_r_ratio)
        else:
            raise ValueError(f"One or both buses '{bus1}', '{bus2}' not found in the circuit.")

    # Add Bundle
    def add_bundle(self, name, num_conductors, spacing, conductor):
        if conductor in self.conductors:
            self.bundles[name] = Bundle(name, num_conductors, spacing, self.conductors[conductor])
        else:
            raise ValueError(f"Conductor '{conductor}' not found. Please add it first.")

    # Add Geometry
    def add_geometry(self, name, xa, ya, xb, yb, xc, yc):
        self.geometries[name] = Geometry(name, xa, ya, xb, yb, xc, yc)

    # Add Transmission Line
    def add_tline(self, name, bus1, bus2, bundle, geometry, length: float, frequency=60):
        if bus1 in self.buses and bus2 in self.buses and bundle in self.bundles and geometry in self.geometries:
            self.tlines[name] = TransmissionLine(name, self.buses[bus1], self.buses[bus2], self.bundles[bundle], self.geometries[geometry], length, frequency)
        else:
            raise ValueError(f"One or more components '{bus1}', '{bus2}', '{bundle}', '{geometry}' are missing from the circuit.")

    # Compute Ybus Admittance Matrix
    def calc_ybus(self):
        num_buses = len(self.buses)
        if num_buses == 0:
            raise ValueError("No buses available to construct Ybus matrix.")
        Ybus_matrix = np.zeros((num_buses, num_buses), dtype=complex)
        bus_list = list(self.buses.keys())

        # Process Transformers
        for tf in self.transformers.values():
            tf_matrix = tf.YPrim_matrix  # Get Yprim matrix
            bus1_idx = bus_list.index(tf.bus1.name)
            bus2_idx = bus_list.index(tf.bus2.name)

            Ybus_matrix[bus1_idx, bus1_idx] += tf_matrix.iloc[0, 0]
            Ybus_matrix[bus1_idx, bus2_idx] += tf_matrix.iloc[0, 1]
            Ybus_matrix[bus2_idx, bus1_idx] += tf_matrix.iloc[1, 0]
            Ybus_matrix[bus2_idx, bus2_idx] += tf_matrix.iloc[1, 1]

        # Process Transmission Lines
        for line in self.tlines.values():
            line_matrix = line.YPrim_matrix  # Get Yprim matrix
            bus1_idx = bus_list.index(line.bus1.name)
            bus2_idx = bus_list.index(line.bus2.name)

            Ybus_matrix[bus1_idx, bus1_idx] += line_matrix.iloc[0, 0]
            Ybus_matrix[bus1_idx, bus2_idx] += line_matrix.iloc[0, 1]
            Ybus_matrix[bus2_idx, bus1_idx] += line_matrix.iloc[1, 0]
            Ybus_matrix[bus2_idx, bus2_idx] += line_matrix.iloc[1, 1]

        # Store Ybus Matrix
        self.ybus = pd.DataFrame(Ybus_matrix, index=bus_list, columns=bus_list)

