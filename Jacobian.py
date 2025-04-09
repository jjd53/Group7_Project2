import numpy as np


class Jacobian:
    def __init__(self, buses, ybus):
        self.buses = buses  # List of bus objects containing type (PQ, PV, Slack)
        self.ybus = ybus  # Admittance matrix (numpy array)

    def calc_jacobian(self, angles, voltages):
        PQ_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PQ Bus']
        PV_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PV Bus']

        all_buses = PQ_buses + PV_buses

        n = len(self.buses)
        m = 2 * len(PQ_buses) + len(PV_buses)  # Adjusted size of the Jacobian

        J1 = self.compute_J1(all_buses, angles, voltages)
        J2 = self.compute_J2(all_buses, angles, voltages)
        J3 = self.compute_J3(all_buses, angles, voltages)
        J4 = self.compute_J4(all_buses, angles, voltages)

        J_top = np.hstack((J1, J2))
        J_bottom = np.hstack((J3, J4))
        J = np.vstack((J_top, J_bottom))

        return J

    def compute_J1(self, buses, angles, voltages):
        """Computes J1 (dP/dδ)"""
        PQ_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PQ Bus']
        PV_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PV Bus']

        all_buses = PQ_buses + PV_buses

        J1 = np.zeros((len(all_buses), len(all_buses)))
        for i, bus_i in enumerate(all_buses):
            for j, bus_j in enumerate(all_buses):
                if i == j:
                    J1[i, j] = -sum(abs(self.ybus[i, k]) * voltages[k] * np.sin(angles[i] - angles[k])
                                    for k in range(len(self.buses)) if k != i)
                else:
                    J1[i, j] = abs(self.ybus[i, j]) * voltages[i] * voltages[j] * np.sin(angles[i] - angles[j])
        return J1

    def compute_J2(self, buses, angles, voltages):
        PQ_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PQ Bus']
        PV_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PV Bus']

        all_buses = PQ_buses + PV_buses

        """Computes J2 (dP/dV)"""
        J2 = np.zeros((len(all_buses), len(PQ_buses)))
        for i, bus_i in enumerate(all_buses):
            for j, bus_j in enumerate(PQ_buses):
                if i == j:
                    J2[i, j] = sum(abs(self.ybus[i, k]) * voltages[k] * np.cos(angles[i] - angles[k])
                                   for k in range(len(self.buses)))
                else:
                    J2[i, j] = abs(self.ybus[i, j]) * voltages[j] * np.cos(angles[i] - angles[j])
        return J2

    def compute_J3(self, buses, angles, voltages):
        PQ_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PQ Bus']
        PV_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PV Bus']

        all_buses = PQ_buses + PV_buses

        """Computes J3 (dQ/dδ)"""
        J3 = np.zeros((len(PQ_buses), len(all_buses)))
        for i, bus_i in enumerate(PQ_buses):
            for j, bus_j in enumerate(all_buses):
                if i == j:
                    J3[i, j] = sum(abs(self.ybus[i, k]) * voltages[k] * np.cos(angles[i] - angles[k])
                                   for k in range(len(self.buses)) if k != i)
                else:
                    J3[i, j] = -abs(self.ybus[i, j]) * voltages[i] * voltages[j] * np.cos(angles[i] - angles[j])
        return J3

    def compute_J4(self, buses, angles, voltages):
        PQ_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PQ Bus']
        PV_buses = [bus for bus in self.buses.values() if bus.bus_type == 'PV Bus']

        all_buses = PQ_buses + PV_buses

        """Computes J4 (dQ/dV)"""
        J4 = np.zeros((len(PQ_buses), len(PQ_buses)))
        for i, bus_i in enumerate(PQ_buses):
            for j, bus_j in enumerate(PQ_buses):
                if i == j:
                    J4[i, j] = -sum(abs(self.ybus[i, k]) * voltages[k] * np.sin(angles[i] - angles[k])
                                    for k in range(len(self.buses)))
                else:
                    J4[i, j] = -abs(self.ybus[i, j]) * voltages[j] * np.sin(angles[i] - angles[j])
        return J4

    def newton_raphson(self, power_mismatch, angles, voltages, tol=1e-3, max_iter=10):
        """Newton-Raphson method to solve power flow equations"""
        for iteration in range(max_iter):
            J = self.calc_jacobian(angles, voltages)
            print("Determinant:", np.linalg.det(J))
            print("Rank:", np.linalg.matrix_rank(J))
            delta_X = np.linalg.solve(J, power_mismatch)

            # Update voltage angles and magnitudes
            for i, bus in enumerate(self.buses):
                if bus.type != 'Slack':
                    angles[i] += delta_X[i]
                    if bus.type == 'PQ':
                        voltages[i] += delta_X[len(self.buses) - 1 + i]

            # Recalculate power mismatch
            power_mismatch = self.calculate_power_mismatch(angles, voltages)

            # Check for convergence
            if np.linalg.norm(power_mismatch, np.inf) < tol:
                print(f'Converged in {iteration + 1} iterations.')
                return angles, voltages

        print('Did not converge within max iterations.')
        return angles, voltages
