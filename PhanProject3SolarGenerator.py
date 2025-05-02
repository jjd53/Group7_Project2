class SolarGenerator:
    def __init__(self, id, bus, capacity_kw, irradiance_factor, efficiency_factor, ambient_temp=25):
        self.id = id
        self.bus = bus
        self.capacity = capacity_kw
        self.irradiance = irradiance_factor
        self.efficiency = efficiency_factor
        self.ambient_temp = ambient_temp  # new!

    def output_power_kw(self):
        temp_coeff = -0.004  # power loss per °C over 25°C
        delta_T = self.ambient_temp - 25
        eff_temp = 1 + temp_coeff * delta_T
        power = self.capacity * self.irradiance * self.efficiency * eff_temp
        return max(power, 0)  # avoid negative output
