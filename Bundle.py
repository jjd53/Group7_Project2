import numpy as np
class Bundle:
    def __init__(self, name, num_conductors, spacing, conductor):
        self.name: str = name
        self.num_conductors: int = num_conductors
        self.spacing: float = spacing
        self.conductor = conductor

    def calcradii(self):

        rc = self.conductor.diam/2
        GMRc = self.conductor.GMR
        d = self.spacing

        if self.num_conductors == 1:
            self.DSC = rc
            self.DSL = GMRc

        if self.num_conductors == 2:
            self.DSC = np.sqrt(rc*d)
            self.DSL = np.sqrt(GMRc*d)

        if self.num_conductors == 3:
            self.DSC = np.cbrt(rc*d**2)
            self.DSL = np.cbrt(GMRc*d**2)

        if self.num_conductors == 4:
            self.DSC = 1.091 * pow(rc*d**3,1/4)
            self.DSL = 1.091 * pow(GMRc*d**3,1/4)

        else:
            pass


