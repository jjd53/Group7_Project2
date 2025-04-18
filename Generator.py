

class Generator:


    def __init__(self, name, bus, Xsub, voltage_setpoint=1.0, mw_setpoint=0.0):

        self.name = name
        self.bus = bus
        self.Xsub = Xsub
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint

    def __repr__(self):
        return (f"Generator(name='{self.name}', bus={self.bus}, "
                f"voltage_setpoint={self.voltage_setpoint} p.u., "
                f"mw_setpoint={self.mw_setpoint} MW)")

if __name__ == "__main__":

    gen1 = Generator(name="Gen1", bus="bus1", voltage_setpoint=1.02, mw_setpoint=100)
    print(gen1)