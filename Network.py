from Circuit import Circuit
from Settings import Settings
from PowerFlowDraftModified import PowerFlow

network = Circuit("network")


network.add_bus("bus1", 20, "Slack Bus")
network.add_bus("bus2", 230, "PQ Bus")
network.add_bus("bus3", 230, "PQ Bus")
network.add_bus("bus4", 230, "PQ Bus")
network.add_bus("bus5", 230, "PQ Bus")
network.add_bus("bus6", 230, "PQ Bus")
network.add_bus("bus7", 18, "PV Bus")

network.add_transformer("T1","bus1", "bus2", 125, 8.5, 10)
network.add_transformer("T2","bus6","bus7", 200, 10.5, 12)

network.add_conductor("Partridge", 0.642, 0.0217, 0.385, 460)
network.add_bundle("Bundle 1", 2, 1.5, "Partridge")
network.add_geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)


network.add_tline("L1","bus2", "bus4", "Bundle 1", "Geometry 1", 10, network.s.frequency)
network.add_tline("L2","bus2", "bus3","Bundle 1", "Geometry 1", 25, network.s.frequency)
network.add_tline("L3","bus3", "bus5","Bundle 1", "Geometry 1", 20, network.s.frequency)
network.add_tline("L4","bus4", "bus6","Bundle 1", "Geometry 1", 20, network.s.frequency)
network.add_tline("L5","bus5", "bus6","Bundle 1", "Geometry 1", 10, network.s.frequency)
network.add_tline("L6","bus4", "bus5","Bundle 1", "Geometry 1", 35, network.s.frequency)

network.add_generator("G1","bus1",1,0)
network.add_generator("G2","bus7",1,200)

network.add_load("Lb3","bus3",110,50)
network.add_load("Lb4","bus4",100,70)
network.add_load("Lb5","bus5",100,65)

network.calc_ybus()
#network.ybus.to_csv("ybus.csv")
#print(network.ybus)
# print(network.ybus)
pf = PowerFlow(network)
pf.run_power_flow()
#print(pf.mismatch*100)
