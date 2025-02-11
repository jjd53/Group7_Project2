from Circuit import Circuit

network = Circuit("network")

network.add_bus("bus1", 20)
network.add_bus("bus2", 230)
network.add_bus("bus3", 230)
network.add_bus("bus4", 230)
network.add_bus("bus5", 230)
network.add_bus("bus6", 230)
network.add_bus("bus7", 18)

network.add_transformer("T1","bus1", "bus2", 125, 8.5, 10)
network.add_transformer("T2","bus6","bus7", 200, 10.5, 12)

network.add_conductor("Partridge", 0.642, 0.0217, 0.385, 460)
network.add_bundle("Bundle 1", 2, 1.5, "Partridge")
network.add_geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)


network.add_tline("L1","bus2", "bus4", "Bundle 1", "Geometry 1", 10, frequency=60)
network.add_tline("L2","bus2", "bus3","Bundle 1", "Geometry 1", 25, frequency=60)
network.add_tline("L3","bus3", "bus5","Bundle 1", "Geometry 1", 20, frequency=60)
network.add_tline("L4","bus4", "bus6","Bundle 1", "Geometry 1", 20, frequency=60)
network.add_tline("L5","bus5", "bus6","Bundle 1", "Geometry 1", 10, frequency=60)
network.add_tline("L6","bus4", "bus5","Bundle 1", "Geometry 1", 35, frequency=60)


print(network.__dict__)
