import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Don't remove, needed for the 3d plot
from simulation import SimRun, Player
from model.galaxyMetrics import Judger
import numpy as np
import config
import os

# simE = Player(path="log/test_2018-10-13 11:31:41.119031_steps_200_stars_100_mass_100000.0_euler.bin")
# simL = Player(path="log/test_2018-10-13 11:32:10.436564_steps_200_stars_100_mass_100000.0_leapfrog.bin")
# simE = Player(path="log/test_2018-10-16 16:58:03.641245_steps_200_stars_100_mass_100000.0_euler.bin")
# simL = Player(path="log/test_2018-10-16 16:58:30.445084_steps_200_stars_100_mass_100000.0_leapfrog.bin")
# These are after refactoring, and yield nice comparison

eulerfilepath =  os.path.join(config.log_dir, 'euler.bin')
leapfrogfilepath =  os.path.join(config.log_dir, 'leapfrog.bin')
hermitefilepath = os.path.join(config.log_dir, 'hermite.bin')

simE = Player(path=eulerfilepath)
simL = Player(path=leapfrogfilepath)
simH = Player(path=hermitefilepath)


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

judgeH = Judger()
while simH.run_step():
    judgeH.metrics(simH.universe)
    judgeH.min_dist(simH.universe)
Hh, Lh = judgeH.metrics(simH.universe)
mindis_h = judgeH.min_dist(simH.universe)

fig, (axH, axL, axD) = plt.subplots(3)

axH.set_title("Hamiltonian")
axL.set_title("Angular Momentum")
axD.set_title("Minimum distance")

t = np.arange(0, len(Ll))

axH.plot(t, He['H'], color='red', label="Euler")
axL.plot(t, Le, color='red', label="Euler")

axH.plot(t, Hl['H'], color='blue', label="Leapfrog")
axL.plot(t, Ll, color='blue', label="Leapfrog")

axH.plot(t, Hh['H'], color='green', label='Hermite')
axL.plot(t, Lh, color='green', label='Hermite')

axD.plot(t, mindis_e, color='red', label='Euler')
axD.plot(t, mindis_l, color='blue', label='Leapfrog')
axD.plot(t, mindis_h, color='green', label='Hermite')

axH.legend()
axL.legend()
axD.legend()

# Use scientific notation for the axis
axH.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
axL.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
axD.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.show()


