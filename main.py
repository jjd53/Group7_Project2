from Bundle import Bundle
from Conductor import Conductor

conductor1 = Conductor("Partridge", 0.642, 0.0217,
0.385, 460)

print(conductor1.name, conductor1.diam,
conductor1.GMR, conductor1.resistance, conductor1.ampacity)

bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
print(bundle1.name, bundle1.num_conductors, bundle1.spacing, bundle1.conductor.name)

