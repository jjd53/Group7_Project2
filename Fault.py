import numpy as np
import pandas as pd


class Fault:

    def __init__(self, circuit, bus, type:str,Zf):
        self.circuit = circuit
        self.Fbus = bus - 1
        self.type = type
        self.Vf = 1
        self.E = np.zeros(len(self.circuit.buses), dtype=complex)
        self.bus_names = list(self.circuit.buses.keys())
        self.ybus = self.circuit.ybus.to_numpy()
        self.Zf = Zf


        self.Y1, self.Y2, self.Y0 = self.build_Yseq()
        self.Z1, self.Z2, self.Z0 = self.seqZbus()

        if type == "3phase":
            self.thrph()
        if type == "ltg":
            self.ltg()
        if type == "ltl":
            self.ltl()
        if type == "dltg":
            self.dltg()

        # self.print_complex_matrix(self.Y1, "Y1 Matrix")
        # self.print_complex_matrix(self.Y2, "Y2 Matrix")
        # self.print_complex_matrix(self.Y0, "Y0 Matrix")

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
        self.SFprint()

    def ltg(self):
        i = self.Fbus
        If = self.Vf / (self.Z0[i, i] + self.Z1[i, i] + self.Z2[i, i] + 3 * self.Zf)
        self.If1 = self.If2 = self.If0 = If
        self.VkFn()
        self.PhVC()
        self.AFprint()

    def ltl(self):
        i = self.Fbus
        self.If1 = self.Vf / (self.Z2[i,i] + self.Z1[i,i] + self.Zf)
        self.If2 = -self.If1
        self.If0 = 0
        self.VkFn()
        self.PhVC()
        self.AFprint()

    def dltg(self):
        i = self.Fbus
        self.If1 = self.Vf / ((self.Z1[i,i])+(self.Z2[i,i]*(self.Z0[i,i]+3*self.Zf))/(self.Z2[i,i]+self.Z0[i,i]+3*self.Zf))
        self.If2 = -self.If1 * ((self.Z0[i,i]+3*self.Zf)/(self.Z0[i,i]+3*self.Zf)+self.Z2[i,i])
        self.If0 = -self.If1 * ((self.Z2[i,i])/(self.Z0[i,i]+3*self.Zf+self.Z2[i,i]))
        self.VkFn()
        self.PhVC()
        self.AFprint()

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
            yprim1 = np.array(gen.yprim1)
            yprim2 = np.array(gen.yprim2)
            yprim0 = np.array(gen.yprim0)
            i = bus_names.index(gen.bus)

            Y1[i, i] += yprim1
            Y2[i, i] += yprim2
            Y0[i, i] += yprim0

        return Y1, Y2, Y0

    def seqZbus(self):
        Z1 = np.linalg.inv(self.Y1)
        Z2 = np.linalg.inv(self.Y2)
        Z0 = np.linalg.inv(self.Y0)
        return Z1, Z2, Z0

    def VkFn(self):
        self.Vk = np.zeros((3,len(self.circuit.buses)),dtype=complex)
        self.I_seq = np.array([self.If0, self.If1, self.If2])  # 1D array shape (3,1)

        for k in range(len(self.circuit.buses)):
            Z_matrix = np.diag([self.Z0[k, self.Fbus], self.Z1[k, self.Fbus], self.Z2[k, self.Fbus]])  # 3x3 diagonal matrix
            self.Vk[:, k] = np.array([0, self.Vf, 0], dtype=complex) - Z_matrix @ self.I_seq

    def PhVC(self):
        self.Vphk = np.zeros((3, len(self.circuit.buses)), dtype=complex)
        self.IphF = np.zeros((3,1),dtype=complex)
        a = 1*np.exp((1j*2*np.pi/3))
        A = np.array(([1,1,1],[1,a**2,a],[1,a,a**2]))
        for k in range(len(self.circuit.buses)):
            self.Vphk[:, k] = A @ self.Vk[:, k]

        self.IphF = A @ self.I_seq

    def SFprint(self):
        print(f"{'Fault Current at Bus':<25} {self.Fbus+1}")
        print(f"{'Magnitude':<15}: {np.abs(self.If):.6f} p.u.")
        print(f"{'Angle':<15}: {np.degrees(np.angle(self.If)):.2f}°\n")

        print(f"{'Bus':<5}{'| Voltage (p.u.)':<20}| Angle (deg)")
        print("-" * 40)
        for i, e in enumerate(self.E, start=1):
            mag = np.abs(e)
            angle = np.degrees(np.angle(e))
            print(f"{i:<5}| {mag:<18.6f}| {angle:.2f}°")

    def AFprint(self):
        print("\n================ Phase Voltages at Buses =================\n")
        for k, bus_name in enumerate(self.bus_names):
            print(f"Bus {bus_name}:")
            for phase in range(3):
                mag = np.abs(self.Vphk[phase, k])
                angle = np.angle(self.Vphk[phase, k], deg=True)
                print(f"  Phase {['A', 'B', 'C'][phase]}: {mag:.4f} ∠ {angle:.2f}°")
            print("-" * 45)

        print("\n================ Fault Phase Currents =================\n")
        for phase in range(3):
            mag = np.abs(self.IphF[phase])
            angle = np.angle(self.IphF[phase], deg=True)
            print(f"Phase {['A', 'B', 'C'][phase]}: {mag:.4f} ∠ {angle:.2f}°")
        print("=" * 55)

    def print_complex_matrix(self, matrix, name="Matrix"):
        print(f"\n{name}:")
        print("-" * (15 * matrix.shape[1]))  # Adjusts line length based on matrix width
        for i in range(matrix.shape[0]):
            row = ""
            for j in range(matrix.shape[1]):
                val = matrix[i, j]
                row += f"{val.real:.4f} + {val.imag:.4f}j\t"  # Format as a + bj
            print(row)
        print("-" * (15 * matrix.shape[1]))



