

class Load:


    def __init__(self, name, bus, real_power=0.0, reactive_power=0.0):

        self.name = name
        self.bus = bus
        self.real_power = real_power
        self.reactive_power = reactive_power

    def __repr__(self):
        return (f"Load(name='{self.name}', bus={self.bus}, "
                f"real_power={self.real_power} MW, "
                f"reactive_power={self.reactive_power} MVar)")


if __name__ == "__main__":

    load1 = Load(name="Load1", bus="bus2", real_power=50, reactive_power=30)
    print(load1)