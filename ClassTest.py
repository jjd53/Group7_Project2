# main.py
from Bus import Bus
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Conductor import Conductor
from Bundle import Bundle
from Geometry import Geometry

if __name__ == "__main__":
    # Bus validation
    bus1 = Bus("Bus 1", 20)
    bus2 = Bus("Bus 2", 230)
    print(f"Bus 1 -> Name: {bus1.name}, Base Voltage: {bus1.base_kv} kV, Index: {bus1.index}")
    print(f"Bus 2 -> Name: {bus2.name}, Base Voltage: {bus2.base_kv} kV, Index: {bus2.index}")

    # Transformer validation
    transformer1 = Transformer("T1", bus1, bus2, 125, 8.5, 10)
    print(f"Transformer -> Name: {transformer1.name}, Bus1: {transformer1.bus1.name}, Bus2: {transformer1.bus2.name}, Power Rating: {transformer1.power_rating} MVA")
    print(f"Impedance (zt): {transformer1.zt} ohms, Admittance (yt): {transformer1.yt} siemens")

    # TransmissionLine validation
    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)
    line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, 10)
    print(f"Transmission Line -> Name: {line1.name}, Bus1: {line1.bus1.name}, Bus2: {line1.bus2.name}, Length: {line1.length} km")
    print(f"Series Impedance: {line1.zseries} ohms, Shunt Admittance: {line1.yshunt} siemens")
