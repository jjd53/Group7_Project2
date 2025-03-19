import numpy as np
import pandas as pd
from Bus import Bus
from Circuit import Circuit


class PowerFlow:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit  # Reference to the system's buses and Ybus
        self.ybus = circuit.ybus.values  # Convert DataFrame to NumPy matrix for calculations
        self.voltages = self._initialize_voltages()
        self.specified_power = self._initialize_specified_power()

    def _initialize_voltages(self):
        voltages = np.ones(len(self.circuit.buses), dtype=complex)
        for i, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "Slack Bus":
                voltages[i] = bus.vpu  # Slack bus voltage is fixed
            elif bus.bus_type == "PV Bus":
                voltages[i] = bus.vpu  # PV buses have a fixed magnitude, but angle varies
            else:
                voltages[i] = 1.0  # PQ buses initial guess is 1.0∠0°
        return voltages

    def _initialize_specified_power(self):
        specified_power = np.zeros(len(self.circuit.buses), dtype=complex)
        for i, bus in enumerate(self.circuit.buses.values()):
            if bus.name in self.circuit.generators:
                generator = self.circuit.generators[bus.name]
                specified_power[i] = complex(generator.mw_setpoint, 0)  # Only real power
            if bus.name in self.circuit.loads:
                load = self.circuit.loads[bus.name]
                specified_power[i] -= complex(load.real_power, load.reactive_power)  # Subtracting load
        return specified_power

    def compute_power_injection(self):
        power_injections = np.zeros(len(self.circuit.buses), dtype=complex)
        for i in range(len(self.circuit.buses)):
            power_injections[i] = self.voltages[i] * np.sum(self.ybus[i, :] * np.conj(self.voltages))
        return power_injections

    def compute_power_mismatch(self)
        power_injections = self.compute_power_injection()
        mismatch = np.zeros(len(self.circuit.buses) * 2 - 1)  # Excluding slack bus ΔQ

        idx = 0
        for i, bus in enumerate(self.circuit.buses.values()):
            if bus.bus_type == "Slack Bus":
                continue  # Slack bus has no mismatch
            mismatch[idx] = self.specified_power[i].real - power_injections[i].real  # ΔP
            idx += 1
            if bus.bus_type == "PQ Bus":
                mismatch[idx] = self.specified_power[i].imag - power_injections[i].imag  # ΔQ
                idx += 1

        return mismatch

    def run_power_flow(self):
        power_injections = self.compute_power_injection()
        mismatch = self.compute_power_mismatch()

        # Display results
        print("\n Power Injections at Buses")
        df_power = pd.DataFrame({
            "Bus": list(self.circuit.buses.keys()),
            "Real Power (P)": power_injections.real,
            "Reactive Power (Q)": power_injections.imag
        })
        print(df_power.round(6))  # Limit decimal places for readability

        print("\n Power Mismatch")
        print(mismatch.round(6))


# Example Usage
if __name__ == "__main__":
    from Network import network  # Import the Circuit instance from Network.py

    power_flow = PowerFlow(network)
    power_flow.run_power_flow()




