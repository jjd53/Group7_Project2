class Bundle:
    def __init__(self, name, num_conductors, spacing, conductor):
        self.name: str = name
        self.num_conductors: int = num_conductors
        self.spacing: float = spacing
        self.conductor = conductor

    def calcradii(self):
        pass