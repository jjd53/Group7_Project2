from Circuit import Circuit
from Bus import Bus
from Transformer_PUS import Transformer
from TransmissionLine_PUS import TransmissionLine
from Conductor import Conductor
from Bundle import Bundle
from Geometry import Geometry

if __name__ == "__main__":
    # Create Circuit
    circuit1 = Circuit("Test Circuit")

    # Add Buses
    circuit1.add_bus("Bus1", 230)
    circuit1.add_bus("Bus2", 115)

    # Add Transformer
    transformer1 = Transformer("T1", circuit1.buses["Bus1"], circuit1.buses["Bus2"], 125, 8.5, 10)
    print("\nTransformer Per-Unit Values:")
    print(f"Rpu: {transformer1.Rpu}, Xpu: {transformer1.Xpu}, Yseries: {transformer1.Yseries}")
    print("\nTransformer Yprim Matrix:")
    print(transformer1.calc_yprim())

    # Create Conductor, Bundle, and Geometry
    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)

    # Add Transmission Line
    line1 = TransmissionLine("Line1", circuit1.buses["Bus1"], circuit1.buses["Bus2"], bundle1, geometry1, 50)
    print("\nTransmission Line Per-Unit Values:")
    print(f"Rpu: {line1.Rpu}, Xpu: {line1.Xpu}, Bpu: {line1.Bpu}")
    print("\nTransmission Line Yprim Matrix:")
    print(line1.calc_yprim())
