from Bundle import Bundle
from Conductor import Conductor
from Geometry import Geometry

conductor1 = Conductor("Partridge", 0.642, 0.0217,
0.385, 460)

print(conductor1.name, conductor1.diam,
conductor1.GMR, conductor1.resistance, conductor1.ampacity)

bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
print(bundle1.name, bundle1.num_conductors, bundle1.spacing, bundle1.conductor.name)

bundle1.calcradii()
print(bundle1.DSC, bundle1.DSL)

geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)
print(geometry1.name, geometry1.xa, geometry1.ya, geometry1.xb, geometry1.yb, geometry1.xc, geometry1.yc)

geometry1.Deq()
print(geometry1.Deq)

