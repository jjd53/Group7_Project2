

class PV_System:

    def __init__(self, name, bus, P, RI, eff):

        self.name = name            #system reference
        self.bus = bus              #bus connection
        self.P = P                  #Power Rating MW
        self.RI = RI                #Relative Irradiance: 0-1
        self.eff = eff              #system efficiency: 0-1

        self.power_gen = self.get_power()

    def get_power(self):

        return -self.P * self.RI * self.eff