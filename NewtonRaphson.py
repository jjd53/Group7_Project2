import numpy as np
from PowerFlowDraftModified import PowerFlow
from Jacobian import Jacobian

class NewtonRaphsonSolver:
    def __init__(self, circuit):
        self.circuit = circuit
        self.power_flow = PowerFlow(circuit)
        self.jacobian = Jacobian(circuit.buses, circuit.ybus.values)
        self.max_iter = 50
        self.tol = 0.001

    def solve(self):
        self.power_flow._initialize_specified_power()

        for iteration in range(self.max_iter):
            self.power_flow.compute_power_injection()
            self.power_flow.compute_power_mismatch()
            mismatch = self.power_flow.mismatch

            print(f"\nIteration {iteration+1}")
            print("Max mismatch:", np.max(np.abs(mismatch)))

            if np.max(np.abs(mismatch)) < self.tol:
                print("Converged!")
                break

            J = self.jacobian.calc_jacobian(self.power_flow.v_angle, self.power_flow.v_magnitude)

            try:
                delta_X = np.linalg.solve(J, mismatch)
            except np.linalg.LinAlgError:
                delta_X = np.linalg.pinv(J) @ mismatch
                print("Jacobian singular, used pseudo-inverse.")

            angle_idx = 0
            volt_idx = 0

            for i, bus in enumerate(self.circuit.buses.values()):
                if bus.bus_type != "Slack Bus":
                    self.power_flow.v_angle[i] += delta_X[angle_idx]
                    angle_idx += 1
                    if bus.bus_type == "PQ Bus":
                        self.power_flow.v_magnitude[i] += delta_X[len(self.circuit.buses) - 1 + volt_idx]
                        volt_idx += 1

        print("\nFinal Voltage Magnitudes:")
        print(self.power_flow.v_magnitude.round(6))

        print("\nFinal Voltage Angles (degrees):")
        print(np.degrees(self.power_flow.v_angle).round(6))


# Example usage
if __name__ == "__main__":
    from Network import network

    solver = NewtonRaphsonSolver(network)
    solver.solve()
