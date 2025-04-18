import numpy as np
import pandas as pd


class Fault:

    def __init__(self, circuit, bus):
        self.circuit = circuit
        self.Fbus = bus - 1
        self.Vf = 1
        self.E = np.zeros(len(self.circuit.buses), dtype=complex)
        bus_names = list(self.circuit.buses.keys())
        self.ybus = self.circuit.ybus.to_numpy()
        for generator in self.circuit.generators.values():
            i = bus_names.index(generator.bus)
            #print(self.ybus[i,i])
            #Xsubpu = generator.Xsub * (self.circuit.buses[generator.bus].base_kv**2)/(230**2)
            self.ybus[i,i] += 1/(1j*generator.Xsub)
            #print(self.ybus[i,i])
        #print(self.ybus)
        self.Zbus = np.linalg.inv(self.ybus)

        self.If = self.Vf/self.Zbus[self.Fbus,self.Fbus]
        for k in range(len(self.circuit.buses)):
            self.E[k] = (1 - (self.Zbus[k,self.Fbus]/self.Zbus[self.Fbus,self.Fbus]))*self.Vf

        print(f"{'Fault Current at Bus':<25} {bus}")
        print(f"{'Magnitude':<15}: {np.abs(self.If):.6f} p.u.")
        print(f"{'Angle':<15}: {np.degrees(np.angle(self.If)):.2f}°\n")

        print(f"{'Bus':<5}{'| Voltage (p.u.)':<20}| Angle (deg)")
        print("-" * 40)
        for i, e in enumerate(self.E, start=1):
            mag = np.abs(e)
            angle = np.degrees(np.angle(e))
            print(f"{i:<5}| {mag:<18.6f}| {angle:.2f}°")



