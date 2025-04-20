import numpy as np
import pandas as pd


class Fault:

    def __init__(self, circuit, bus, type:str):
        self.circuit = circuit
        self.Fbus = bus - 1
        self.type = type
        self.Vf = 1
        self.E = np.zeros(len(self.circuit.buses), dtype=complex)
        self.bus_names = list(self.circuit.buses.keys())
        self.ybus = self.circuit.ybus.to_numpy()


        self.Y1, self.Y2, self.Y0 = self.build_Yseq()

        if type == "3phase":
            self.thrph()
        if type == "ltg":
            self.ltg()

    def thrph(self):
        for generator in self.circuit.generators.values():
            i = self.bus_names.index(generator.bus)
            #print(self.ybus[i,i])
            #Xsubpu = generator.Xsub * (self.circuit.buses[generator.bus].base_kv**2)/(230**2)
            self.ybus[i,i] += 1/(1j*generator.Xsub)
            #print(self.ybus[i,i])
        #print(self.ybus)
        self.Zbus = np.linalg.inv(self.ybus)

        self.If = self.Vf/self.Zbus[self.Fbus,self.Fbus]
        for k in range(len(self.circuit.buses)):
            self.E[k] = (1 - (self.Zbus[k,self.Fbus]/self.Zbus[self.Fbus,self.Fbus]))*self.Vf
        self.Fprint()

    def ltg(self):
        print("Yes")

    def ltl(self):
        return

    def dltg(self):
        return

    def build_Yseq(self):
        num_buses = len(self.circuit.buses)
        bus_names = list(self.circuit.buses.keys())

        # Initialize an empty Ybus matrix
        Y1 = np.zeros((num_buses, num_buses), dtype=complex)
        Y2 = np.zeros((num_buses, num_buses), dtype=complex)
        Y0 = np.zeros((num_buses, num_buses), dtype=complex)

        for transformer in self.circuit.transformers.values():
            yprim1 = np.array(transformer.yprim1)
            yprim2 = np.array(transformer.yprim2)
            yprim0 = np.array(transformer.yprim0)

            i = bus_names.index(transformer.bus1.name)
            j = bus_names.index(transformer.bus2.name)


            Y1[i, i] += yprim1[0, 0]
            Y1[i, j] += yprim1[0, 1]
            Y1[j, i] += yprim1[1, 0]
            Y1[j, j] += yprim1[1, 1]

            Y2[i, i] += yprim2[0, 0]
            Y2[i, j] += yprim2[0, 1]
            Y2[j, i] += yprim2[1, 0]
            Y2[j, j] += yprim2[1, 1]

            Y0[i, i] += yprim0[0, 0]
            Y0[i, j] += yprim0[0, 1]
            Y0[j, i] += yprim0[1, 0]
            Y0[j, j] += yprim0[1, 1]

        for line in self.circuit.tlines.values():
            yprim1 = np.array(line.yprim1)
            yprim2 = np.array(line.yprim2)
            yprim0 = np.array(line.yprim0)
            i = bus_names.index(line.bus1)
            j = bus_names.index(line.bus2)

            # Add admittances to Ybus
            Y1[i, i] += yprim1[0, 0]
            Y1[i, j] += yprim1[0, 1]
            Y1[j, i] += yprim1[1, 0]
            Y1[j, j] += yprim1[1, 1]

            Y2[i, i] += yprim2[0, 0]
            Y2[i, j] += yprim2[0, 1]
            Y2[j, i] += yprim2[1, 0]
            Y2[j, j] += yprim2[1, 1]

            Y0[i, i] += yprim0[0, 0]
            Y0[i, j] += yprim0[0, 1]
            Y0[j, i] += yprim0[1, 0]
            Y0[j, j] += yprim0[1, 1]


        # --- Generators ---
        for gen in self.circuit.generators.values():
            yprim1 = np.array(line.yprim1)
            yprim2 = np.array(line.yprim2)
            yprim0 = np.array(line.yprim0)
            i = bus_names.index(line.bus1)

            Y1[i, i] += yprim1[0, 0]
            Y2[i, i] += yprim2[0, 0]
            Y0[i, i] += yprim0[0, 0]

        return Y1, Y2, Y0

    def Fprint(self):
        print(f"{'Fault Current at Bus':<25} {self.Fbus-1}")
        print(f"{'Magnitude':<15}: {np.abs(self.If):.6f} p.u.")
        print(f"{'Angle':<15}: {np.degrees(np.angle(self.If)):.2f}°\n")

        print(f"{'Bus':<5}{'| Voltage (p.u.)':<20}| Angle (deg)")
        print("-" * 40)
        for i, e in enumerate(self.E, start=1):
            mag = np.abs(e)
            angle = np.degrees(np.angle(e))
            print(f"{i:<5}| {mag:<18.6f}| {angle:.2f}°")



