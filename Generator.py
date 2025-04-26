

class Generator:


    def __init__(self, name, bus, Xsub, X2, X0, Zg=0, grounded=True, voltage_setpoint=1.0, mw_setpoint=0.0):

        self.name = name
        self.bus = bus
        self.Xsub = Xsub
        self.X2 = X2
        self.X0 = X0
        self.Zg = Zg
        self.grounded = grounded
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint
        self.Y1, self.Y2, self.Y0 = self.get_sequence_admittances()
        self.calc_yprim_seq()

    def get_sequence_admittances(self):
        Y1 = 1 / (1j * self.Xsub)
        Y2 = 1 / (1j * self.X2)
        if self.grounded:
            Y0 = 1 / (1j * self.X0 +  self.Zg)
        else:
            Y0 = 0
        return Y1, Y2, Y0

    def calc_yprim_seq(self):

        self.yprim1 = [self.Y1]
        self.yprim2 = [self.Y2]
        self.yprim0 = [self.Y0]

    def __repr__(self):
        return (f"Generator(name='{self.name}', bus={self.bus}, "
                f"voltage_setpoint={self.voltage_setpoint} p.u., "
                f"mw_setpoint={self.mw_setpoint} MW)")

if __name__ == "__main__":

    gen1 = Generator(name="Gen1", bus="bus1", voltage_setpoint=1.02, mw_setpoint=100)
    print(gen1)