import numpy as np
import pandas as pd

class SymmetricalFaultAnalyzer:
    def __init__(self, circuit):
        self.circuit = circuit
        self.ybus = circuit.ybus.copy()
        self.zbus = None

    def _convert_generator_reactance_to_system_base(self, gen_reactance, gen_base_MVA, system_base_MVA):
        """
        Converts generator subtransient reactance to system base.
        """
        return gen_reactance * (system_base_MVA / gen_base_MVA)

    def _add_generator_subtransient_admittance(self):
        """
        Adds generator subtransient admittances to the diagonal of Ybus.
        """
        for gen_name, gen in self.circuit.generators.items():
            if hasattr(gen, 'x_double_prime'):
                x_pp_system = self._convert_generator_reactance_to_system_base(
                    gen.x_double_prime, gen.base_MVA, self.circuit.s.base_power
                )
                y_gen = 1 / (1j * x_pp_system)

                if gen.bus in self.ybus.columns:
                    self.ybus.loc[gen.bus, gen.bus] += y_gen
                else:
                    raise ValueError(f"Bus {gen.bus} for generator {gen.name} not found in Ybus.")

    def calculate_zbus(self):
        """
        Inverts Ybus to get Zbus.
        """
        self._add_generator_subtransient_admittance()
        self.zbus = pd.DataFrame(np.linalg.inv(self.ybus.values), 
                                 index=self.ybus.index, columns=self.ybus.columns)
        return self.zbus

    def calculate_fault_current(self, faulted_bus, pre_fault_voltage=1.0):
        """
        Calculates the subtransient fault current for a bolted three-phase fault.
        """
        if self.zbus is None:
            self.calculate_zbus()

        Znn = self.zbus.loc[faulted_bus, faulted_bus]
        Ifault = pre_fault_voltage / Znn
        return Ifault

    def calculate_post_fault_voltages(self, faulted_bus, pre_fault_voltage=1.0):
        """
        Calculates post-fault bus voltages.
        """
        if self.zbus is None:
            self.calculate_zbus()

        Znn = self.zbus.loc[faulted_bus, faulted_bus]
        voltages = {}
        for bus in self.zbus.index:
            Zkn = self.zbus.loc[bus, faulted_bus]
            voltages[bus] = pre_fault_voltage - (Zkn / Znn) * pre_fault_voltage
        return voltages


# Example Usage
if __name__ == "__main__":
    from Network import network  # Assumes network has been built as in Network.py

    # Set generator subtransient reactance (in generator base MVA)
    network.generators["G1"].x_double_prime = 0.2  # Typical example values
    network.generators["G1"].base_MVA = 100
    network.generators["G2"].x_double_prime = 0.2
    network.generators["G2"].base_MVA = 100

    fault_analysis = SymmetricalFaultAnalyzer(network)
    zbus = fault_analysis.calculate_zbus()

    faulted_bus = "bus7"
    Ifault = fault_analysis.calculate_fault_current(faulted_bus)
    voltages = fault_analysis.calculate_post_fault_voltages(faulted_bus)

    print("\nZbus Matrix:")
    print(np.round(zbus, 4))
    print(f"\n Fault current at {faulted_bus}: {Ifault:.4f} pu")
    print("\n Post-Fault Voltages:")
    for bus, v in voltages.items():
        print(f"{bus}: {v:.4f} pu")
