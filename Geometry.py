import numpy as np
class Geometry:
    def __init__(self, name, xa, ya, xb, yb, xc, yc):
        self.name: str = name
        self.xa: float = xa
        self.ya: float = ya
        self.xb: float = xb
        self.yb: float = yb
        self.xc: float = xc
        self.yc: float = yc
        self.Deq()

    def Deq(self):

        Dab = np.sqrt((self.xb - self.xa)**2 + (self.yb - self.ya)**2)
        Dbc = np.sqrt((self.xc - self.xb) ** 2 + (self.yc - self.yb) ** 2)
        Dca = np.sqrt((self.xa - self.xc) ** 2 + (self.ya - self.yc) ** 2)

        self.Deq = np.cbrt(Dab * Dbc * Dca)

