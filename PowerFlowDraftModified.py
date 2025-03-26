import numpy as np
import pandas as pd
from Bus import Bus
from Circuit import Circuit
from Settings import Settings

class PowerFlow:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.ybus = circuit.ybus.values
        self.Sbase = circuit.s.base_power

        self.v_magnitude = np.ones(len(self.circuit.buses))
        self.v_angle = np.zeros(len(self.circuit.buses))  # in radians

        self.specified_power = self._initialize_specified_power()

    def _initialize_specified_power(self):
        specified_power = np.zeros(len(self.circuit.buses), dtype=complex)

        for i, bus in enumerate(self.circuit.buses.values()):
            for gn in self.circuit.generators:
                if self.circuit.generators[gn].bus == bus.name:
                    gen = self.circuit.generators[gn]
                    specified_power[i] += complex(gen.mw_setpoint, 0) / self.Sbase
            for ld in self.circuit.loads:
                if self.circuit.loads[ld].bus == bus.name:
                    load = self.circuit.loads[ld]
                    specified_power[i] -= complex(load.real_power, load.reactive_power) / self.Sbase
        return specified_power

    def compute_power_injection(self):
        P = np.zeros(len(self.circuit.buses))
        Q = np.zeros(len(self.circuit.buses))
        G = self.ybus.real
        B = self.ybus.imag

        for i in range(len(self.circuit.buses)):
            for j in range(len(self.circuit.buses)):
                angle_diff = self.v_angle[i] - self.v_angle[j]
                P[i] += self.v_magnitude[i] * self.v_magnitude[j] * (G[i, j] * np.cos(angle_diff) + B[i, j] * np.sin(angle_diff))
                Q[i] += self.v_magnitude[i] * self.v_magnitude[j] * (G[i, j] * np.sin(angle_diff) - B[i, j] * np.cos(angle_diff))
        return P, Q

    def compute_power_mismatch(self):
        P_calc, Q_calc = self.compute_power_injection()
        mismatch = np.zeros(len(self.circuit.buses) * 2)

        idx = 0
        for i, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "Slack Bus":
                continue
            mismatch[idx] = self.specified_power[i].real - P_calc[i]
            idx += 1
            if bus.bus_type == "PQ Bus":
                mismatch[idx] = self.specified_power[i].imag - Q_calc[i]
                idx += 1
        return mismatch

    def run_power_flow(self):
        P_calc, Q_calc = self.compute_power_injection()
        mismatch = self.compute_power_mismatch()

        print("\nPower Injections at Each Bus:")
        print("Bus\tP_inj (p.u.)\tQ_inj (p.u.)")
        print("-" * 40)
        for i, (bus_name, bus) in enumerate(self.circuit.buses.items()):
            print(f"{bus_name}\t{P_calc[i]:.4f}\t\t{Q_calc[i]:.4f}")

        print("\nPower Mismatch Results:")
        idx = 0
        for i, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "Slack Bus":
                continue
            dP = mismatch[idx]
            idx += 1
            if bus.bus_type == "PQ Bus":
                dQ = mismatch[idx]
                idx += 1
            else:
                dQ = 0.0
            print(f"Bus {bus.name}: \u0394P = {dP:.4f} p.u., \u0394Q = {dQ:.4f} p.u.")


if __name__ == "__main__":
    from Network import network
    pf = PowerFlow(network)
    pf.run_power_flow()
