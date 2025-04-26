from Circuit import Circuit
from Settings import Settings
from PowerFlowDraftModified import PowerFlow
from Jacobian import Jacobian
from NewtonRaphson import NewtonRaphsonSolver
from Fault import Fault

network = Circuit("network")


network.add_bus("bus1", 20, "Slack Bus")
network.add_bus("bus2", 230, "PQ Bus")
network.add_bus("bus3", 230, "PQ Bus")
network.add_bus("bus4", 230, "PQ Bus")
network.add_bus("bus5", 230, "PQ Bus")
network.add_bus("bus6", 230, "PQ Bus")
network.add_bus("bus7", 18, "PV Bus")

network.add_transformer("T1","bus1", "bus2", 125, 8.5, 10,"D-Y",0.0019)
network.add_transformer("T2","bus6","bus7", 200, 10.5, 12, "D-Y", 1e15)

network.add_conductor("Partridge", 0.642, 0.0217, 0.385, 460)
network.add_bundle("Bundle 1", 2, 1.5, "Partridge")
network.add_geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)


network.add_tline("L1","bus2", "bus4", "Bundle 1", "Geometry 1", 10, network.s.frequency)
network.add_tline("L2","bus2", "bus3","Bundle 1", "Geometry 1", 25, network.s.frequency)
network.add_tline("L3","bus3", "bus5","Bundle 1", "Geometry 1", 20, network.s.frequency)
network.add_tline("L4","bus4", "bus6","Bundle 1", "Geometry 1", 20, network.s.frequency)
network.add_tline("L5","bus5", "bus6","Bundle 1", "Geometry 1", 10, network.s.frequency)
network.add_tline("L6","bus4", "bus5","Bundle 1", "Geometry 1", 35, network.s.frequency)

network.add_generator("G1","bus1",0.12, 0.14, 0.05,0, True,1,0)
network.add_generator("G2","bus7",0.12,0.14, 0.05,0.3086,True,1,200)

network.add_load("Lb3","bus3",110,50)
network.add_load("Lb4","bus4",100,70)
network.add_load("Lb5","bus5",100,65)

network.calc_ybus()
#network.ybus.to_csv("ybus.csv")

#print(network.ybus)

#NewtonRaphsonSolver(network)

Fault(network,2,"3phase")


# pf = PowerFlow(network)
# pf.run_power_flow()
# jac=Jacobian(pf.circuit.buses,pf.ybus)
# jac.calc_jacobian(pf.v_angle,pf.v_magnitude)
# jac.newton_raphson(pf.mismatch,pf.v_angle,pf.v_magnitude)
# #print(pf.circuit.ybus)
# print(pf.mismatch)
# print(pf.v_angle)
# print(pf.v_magnitude)


#print(pf.mismatch*100)
