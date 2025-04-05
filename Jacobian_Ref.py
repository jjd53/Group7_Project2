import numpy as np
import pandas as pd

class Jacobian:
    def __init__(self, buses, ybus):
        self.buses = list(buses.values())
        self.bus_names = [bus.name for bus in self.buses]
        self.ybus = ybus.values  # numpy array
        self.num_buses = len(self.buses)

    def calc_jacobian(self, voltages, angles):
        V = np.array(voltages)
        delta = np.radians(angles)
        G = self.ybus.real
        B = self.ybus.imag

        J1 = np.zeros((self.num_buses, self.num_buses))  # dP/dDelta
        J2 = np.zeros((self.num_buses, self.num_buses))  # dP/dV
        J3 = np.zeros((self.num_buses, self.num_buses))  # dQ/dDelta
        J4 = np.zeros((self.num_buses, self.num_buses))  # dQ/dV

        for i in range(self.num_buses):
            for j in range(self.num_buses):
                if i == j:
                    
                    for k in range(self.num_buses):
                        if k != i:
                            J1[i][j] += V[i] * V[k] * (
                                G[i][k] * np.sin(delta[i] - delta[k]) -
                                B[i][k] * np.cos(delta[i] - delta[k])
                            )
                            J3[i][j] += -V[i] * V[k] * (
                                G[i][k] * np.cos(delta[i] - delta[k]) +
                                B[i][k] * np.sin(delta[i] - delta[k])
                            )
                    J2[i][j] = V[i] * G[i][i] + sum([
                        V[k] * (G[i][k] * np.cos(delta[i] - delta[k]) +
                                B[i][k] * np.sin(delta[i] - delta[k]))
                        for k in range(self.num_buses) if k != i])
                    J4[i][j] = -V[i] * B[i][i] + sum([
                        V[k] * (G[i][k] * np.sin(delta[i] - delta[k]) -
                                B[i][k] * np.cos(delta[i] - delta[k]))
                        for k in range(self.num_buses) if k != i])
                else:
                    
                    J1[i][j] = -V[i] * V[j] * (
                        G[i][j] * np.sin(delta[i] - delta[j]) -
                        B[i][j] * np.cos(delta[i] - delta[j])
                    )
                    J2[i][j] = V[i] * (G[i][j] * np.cos(delta[i] - delta[j]) +
                                      B[i][j] * np.sin(delta[i] - delta[j]))

                    J3[i][j] = -V[i] * V[j] * (
                        G[i][j] * np.cos(delta[i] - delta[j]) +
                        B[i][j] * np.sin(delta[i] - delta[j])
                    )
                    J4[i][j] = V[i] * (G[i][j] * np.sin(delta[i] - delta[j]) -
                                      B[i][j] * np.cos(delta[i] - delta[j]))

        
        rows, cols = [], []
        for i, bus in enumerate(self.buses):
            if bus.bus_type != "Slack Bus":
                rows.append(i)
                cols.append(i)  # dP/dDelta and dQ/dDelta (no delta for Slack)
        J1 = J1[np.ix_(rows, cols)]
        J2 = J2[np.ix_(rows, cols)]

        Q_rows, Q_cols = [], []
        for i, bus in enumerate(self.buses):
            if bus.bus_type == "PQ Bus":
                Q_rows.append(i)
                Q_cols.append(i)  # only V for PQ
        J3 = J3[np.ix_(Q_rows, cols)]
        J4 = J4[np.ix_(Q_rows, Q_cols)]

        # Stack to form full Jacobian
        top = np.hstack((J1, J2))
        bottom = np.hstack((J3, J4))
        self.J = np.vstack((top, bottom))


