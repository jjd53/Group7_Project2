import numpy as np
from Circuit import Circuit

class PowerFlow:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.ybus = circuit.ybus.values
        self.Sbase = circuit.s.base_power
        self.v_magnitude = np.ones(len(self.circuit.buses))
        self.v_angle = np.zeros(len(self.circuit.buses))  # in radians
        #self.v_magnitude = [1,0.9369,0.92047,0.92978,0.92671,0.93966,0.99999]
        #self.v_angle = [0,-0.0776035,-0.0954169,-0.0821253,-0.0844165,-0.0690142,0.0375055]
        self.mismatch = np.ones(11)
        self.P = np.zeros(len(self.circuit.buses))
        self.Q = np.zeros(len(self.circuit.buses))

    def _initialize_specified_power(self):
        self.specified_power = np.zeros(len(self.circuit.buses), dtype=complex)

        for i, bus in enumerate(self.circuit.buses.values()):
            for gn in self.circuit.generators:
                if self.circuit.generators[gn].bus == bus.name:
                    gen = self.circuit.generators[gn]
                    self.specified_power[i] += complex(gen.mw_setpoint, 0) / self.Sbase
            for ld in self.circuit.loads:
                if self.circuit.loads[ld].bus == bus.name:
                    load = self.circuit.loads[ld]
                    self.specified_power[i] += complex(-load.real_power, -load.reactive_power) / self.Sbase

    # def compute_power_injection(self):
    #     self.P = np.zeros(len(self.circuit.buses))
    #     self.Q = np.zeros(len(self.circuit.buses))
    #
    #     V_complex = self.v_magnitude * np.exp(1j * self.v_angle)  # Convert to complex voltage
    #
    #     S_injected = V_complex * np.conjugate(self.ybus @ V_complex)  # Power injection using Y-bus
    #     self.P = S_injected.real
    #     self.Q = S_injected.imag

    def compute_power_injection(self):

        yabs = np.abs(self.ybus)
        yangle = np.angle(self.ybus)

        for i in range(len(self.circuit.buses)):
            for j in range(len(self.circuit.buses)):
                angle_diff = self.v_angle[i] - self.v_angle[j] - yangle[i,j]
                Qu = self.v_magnitude[i] * self.v_magnitude[j] * yabs[i,j] * np.sin(angle_diff)
                Pu = self.v_magnitude[i] * self.v_magnitude[j] * yabs[i,j] * np.cos(angle_diff)
                self.Q[i] += Qu
                self.P[i] += Pu
        #return self.P,self.Q
                # if i == 1 or i == 2:
                #     print(" bus= ", i+1, " j= ", j," Q= ", Qu," P= ", Pu)
    def compute_power_mismatch(self):



        idx = 0
        for i, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "Slack Bus":
                #idx += 1
                continue
            self.mismatch[idx] = self.specified_power[i].real - self.P[i]
            idx += 1

        idx = 0
        for i, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "Slack Bus":
                # idx += 1
                continue
            if bus.bus_type == "PQ Bus":
                self.mismatch[idx + 6] = self.specified_power[i].imag - self.Q[i]
            idx += 1
        #print(len(self.mismatch))

    # def compute_power_mismatch(self):
    #
    #     self.mismatch = np.zeros(len(self.circuit.buses) * 2)
    #
    #     idx = 0
    #     for i, bus in enumerate(self.circuit.buses.values()):
    #         if bus.bus_type == "Slack Bus":
    #             continue
    #         self.mismatch[idx] = self.specified_power[i].real - self.P[i]
    #
    #         if bus.bus_type == "PQ Bus":
    #             self.mismatch[idx+len(self.circuit.buses)] = self.specified_power[i].imag - self.Q[i]
    #         idx += 1

    def run_power_flow(self):
        self._initialize_specified_power()
        self.compute_power_injection()
        self.compute_power_mismatch()

        # print("\nPower Injections at Each Bus:")
        # print("Bus\tP_inj (p.u.)\tQ_inj (p.u.)")
        # print("-" * 40)
        # for i, (bus_name, bus) in enumerate(self.circuit.buses.items()):
        #     print(f"{bus_name}\t{self.P[i]:.4f}\t\t{self.Q[i]:.4f}")
        #print(self.specified_power)
        print("Updated Computed Power Injection (P):", self.P)
        print("Updated Computed Power Injection (Q):", self.Q)
        print("Updated Mismatch Vector:", self.mismatch)

        # print("\nPower Mismatch Results:")
        #
        # for i, bus in enumerate(self.circuit.buses.values()):
        #
        #     dP = self.mismatch[i+1]
        #
        #     dQ = self.mismatch[i+1+len(self.circuit.buses)-1]
        #
        #     print(f"Bus {bus.name}: \u0394P = {dP:.4f} p.u., \u0394Q = {dQ:.4f} p.u.")


# if __name__ == "__main__":
#     from Network import network
#     pf = PowerFlow(network)
#     pf.run_power_flow()
