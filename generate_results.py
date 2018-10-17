from simulation import SimRun, Player
from simulation import Euler, Leapfrog, Hermite
from model import Universe
import copy

# Integrator comparison
u1 = Universe(n_stars=100)
u2 = copy.deepcopy(u1)
# u3 = copy.deepcopy(u1)

# Simulate 500 steps with Euler
sim1 = SimRun(n_steps=200, universe=u1, integrator=Euler())
sim1.run()
sim2 = SimRun(n_steps=200, universe=u2, integrator=Leapfrog())
sim2.run()
# sim3 = SimRun(n_steps=200, universe=u3, integrator=Hermite())
# sim3.run()

