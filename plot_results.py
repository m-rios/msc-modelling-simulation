import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Don't remove, needed for the 3d plot
from simulation import SimRun, Player
from model.galaxyMetrics import Judger
import numpy as np

# simE = Player(path="log/test_2018-10-13 11:31:41.119031_steps_200_stars_100_mass_100000.0_euler.bin")
# simL = Player(path="log/test_2018-10-13 11:32:10.436564_steps_200_stars_100_mass_100000.0_leapfrog.bin")
# simE = Player(path="log/test_2018-10-16 16:58:03.641245_steps_200_stars_100_mass_100000.0_euler.bin")
# simL = Player(path="log/test_2018-10-16 16:58:30.445084_steps_200_stars_100_mass_100000.0_leapfrog.bin")
# These are after refactoring, and yield nice comparison
simE = Player(path="results/test_2018-10-16 17:19:01.611315_steps_200_stars_100_mass_100000.0_euler.bin")
simL = Player(path="results/test_2018-10-16 17:19:26.833448_steps_200_stars_100_mass_100000.0_leapfrog.bin")

judgeE = Judger()
while simE.run_step():
    judgeE.metrics(simE.universe)
    judgeE.min_dist(simE.universe)
He, Le = judgeE.metrics(simE.universe)
mindis_e = judgeE.min_dist(simE.universe)

judgeL = Judger()
while simL.run_step():
    judgeL.metrics(simL.universe)
    judgeL.min_dist(simL.universe)
Hl, Ll = judgeL.metrics(simL.universe)
mindis_l = judgeL.min_dist(simL.universe)

fig, (axH, axL, axD) = plt.subplots(3)

axH.set_title("Hamiltonian")
axL.set_title("Angular Momentum")
axD.set_title("Minimum distance")

t = np.arange(0, len(Ll))

axH.plot(t, He['H'], color='red', label="Euler")
axL.plot(t, Le, color='red', label="Euler")

axH.plot(t, Hl['H'], color='blue', label="Leapfrog")
axL.plot(t, Ll, color='blue', label="Leapfrog")

axD.plot(t, mindis_e, color='red', label='Euler')
axD.plot(t, mindis_l, color='blue', label='Leapfrog')

axH.legend()
axL.legend()
axD.legend()

# Use scientific notation for the axis
axH.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
axL.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
axD.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.show()

pass

