
import numpy as np
import pandas as pd

class SequenceBuilder:
    def __init__(self, circuit):
        self.circuit = circuit
        self.bus_names = list(circuit.buses.keys())
        self.n = len(self.bus_names)

        # Initialize empty Ybus matrices
        self.Ybus_pos = np.zeros((self.n, self.n), dtype=complex)
        self.Ybus_neg = np.zeros((self.n, self.n), dtype=complex)
        self.Ybus_zero = np.zeros((self.n, self.n), dtype=complex)

        self.build_sequence_networks()

    def build_sequence_networks(self):
        self.add_generators()
        self.add_transformers()
        self.add_transmission_lines()

        # Invert to obtain Zbus
        self.Zbus_pos = np.linalg.inv(self.Ybus_pos)
        self.Zbus_neg = np.linalg.inv(self.Ybus_neg)
        self.Zbus_zero = np.linalg.inv(self.Ybus_zero)

    def add_generators(self):
        for gen in self.circuit.generators.values():
            i = self.bus_names.index(gen.bus)
            self.Ybus_pos[i, i] += 1 / (1j * gen.Xsub)  # positive-sequence
            self.Ybus_neg[i, i] += 1 / (1j * gen.Xneg)  # negative-sequence
            if gen.grounded:
                self.Ybus_zero[i, i] += 1 / (1j * gen.Xzero + gen.grounding_impedance)  # zero-sequence with ground


    def add_transformers(self):
        for tx in self.circuit.transformers.values():
            i = self.bus_names.index(tx.bus1.name)
            j = self.bus_names.index(tx.bus2.name)

            # For now, reuse the positive-sequence for negative-sequence
            Ytx = 1 / complex(tx.Rpu, tx.Xpu)

            self.Ybus_pos[i, i] += Ytx
            self.Ybus_pos[j, j] += Ytx
            self.Ybus_pos[i, j] -= Ytx
            self.Ybus_pos[j, i] -= Ytx

            self.Ybus_neg[i, i] += Ytx
            self.Ybus_neg[j, j] += Ytx
            self.Ybus_neg[i, j] -= Ytx
            self.Ybus_neg[j, i] -= Ytx

            if tx.connection in ["Y-Y", "Y-Delta", "Delta-Y"]:
                # Only Y-connected transformers with ground contribute to zero-sequence
                if tx.Zgnd == 0:
                    continue  # ungrounded
                Yz = 1 / (3 * (1j * tx.Xzero + tx.Zgnd))
                self.Ybus_zero[i, i] += Yz
                self.Ybus_zero[j, j] += Yz
                self.Ybus_zero[i, j] -= Yz
                self.Ybus_zero[j, i] -= Yz

    def add_transmission_lines(self):
        for line in self.circuit.tlines.values():
            i = self.bus_names.index(line.bus1)
            j = self.bus_names.index(line.bus2)

            Yline_pos = 1 / complex(line.r_pos, line.x_pos)
            Yline_neg = Yline_pos
            Yline_zero = 1 / complex(line.r_zero, line.x_zero)

            for Y, Ybus in zip([Yline_pos, Yline_neg, Yline_zero],
                               [self.Ybus_pos, self.Ybus_neg, self.Ybus_zero]):
                Ybus[i, i] += Y
                Ybus[j, j] += Y
                Ybus[i, j] -= Y
                Ybus[j, i] -= Y

    def export_Ybus_matrices(self):
        return {
            "positive": pd.DataFrame(self.Ybus_pos, index=self.bus_names, columns=self.bus_names),
            "negative": pd.DataFrame(self.Ybus_neg, index=self.bus_names, columns=self.bus_names),
            "zero": pd.DataFrame(self.Ybus_zero, index=self.bus_names, columns=self.bus_names),
        }

    def export_Zbus_matrices(self):
        return {
            "positive": pd.DataFrame(self.Zbus_pos, index=self.bus_names, columns=self.bus_names),
            "negative": pd.DataFrame(self.Zbus_neg, index=self.bus_names, columns=self.bus_names),
            "zero": pd.DataFrame(self.Zbus_zero, index=self.bus_names, columns=self.bus_names),
        }
