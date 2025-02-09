from Circuit import Circuit


circuit1 = Circuit("Test Circuit")
print(circuit1.name)  # Expected output: "Test Circuit"
print(type(circuit1.name)) # Expected output: <class ‘str’>
print(circuit1.buses)  # Expected output: {}
print(type(circuit1.buses)) # Expected output: <class ‘dict’>

circuit1.add_bus("Bus1", 230)
print(type(circuit1.buses["Bus1"])) # Expected output: <class ‘Bus.Bus’>
print(circuit1.buses["Bus1"].name ,circuit1.buses["Bus1"].base_kv)  # Expected output: "Bus1", 230

print("Buses in circuit:", list(circuit1.buses.keys()))  # Expected output: ["Bus1"]