# Bus.py
class Bus:
    bus_count = 0  

    VALID_BUS_TYPES = ["Slack Bus", "PQ Bus", "PV Bus"]

    def __init__(self, name: str, base_kv: float,bus_type:str, vpu = 1.0,delta = 0.0):
        self.name = name
        self.base_kv = base_kv
        self.bus_type = bus_type
        self.vpu = vpu
        self.delta = delta
        self.index = Bus.bus_count
        Bus.bus_count += 1

        self._validate_bus_type()

    def _validate_bus_type(self):
        """Ensure the bus type is valid."""
        if self.bus_type not in self.VALID_BUS_TYPES:
            raise ValueError(f"Invalid bus type: '{self.bus_type}'. "
                             f"Valid options are: {', '.join(self.VALID_BUS_TYPES)}.")