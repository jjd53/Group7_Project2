from Circuit_Ybus import Circuit_Ybus

if __name__ == "__main__":

    circuit1 = Circuit_Ybus("Test Circuit")


    circuit1.add_bus("Bus1", 230)
    circuit1.add_bus("Bus2", 115)


    circuit1.add_conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    circuit1.add_bundle("Bundle1", 2, 1.5, "Partridge")
    circuit1.add_geometry("Geometry1", 0, 0, 18.5, 0, 37, 0)


    circuit1.add_transformer("T1", "Bus1", "Bus2", 125, 8.5, 10, 1.0, 1.0)


    transformer1 = circuit1.transformers["T1"]
    print("\n Transformer Per-Unit Values:")
    print(f"Rpu: {transformer1.Rpu}, Xpu: {transformer1.Xpu}, Yseries: {transformer1.Yseries}")

    print("\n Transformer Yprim Matrix:")
    print(transformer1.YPrim_matrix)


    circuit1.add_tline("Line1", "Bus1", "Bus2", "Bundle1", "Geometry1", 50)


    line1 = circuit1.tlines["Line1"]
    print("\n Transmission Line Per-Unit Values:")
    print(f"Rpu: {line1.Rpu}, Xpu: {line1.Xpu}, Bpu: {line1.Bpu}")

    print("\n Transmission Line Yprim Matrix:")
    print(line1.YPrim_matrix)


    circuit1.calc_ybus()
    print("\n Final System-Wide Ybus Matrix:")
    print(circuit1.ybus)
