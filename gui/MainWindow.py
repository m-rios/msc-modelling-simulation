import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Don't remove, needed for the 3d plot
from matplotlib.animation import FuncAnimation
from simulation import SimRun, Player, Simulator
from model.galaxyMetrics import Judger
import numpy as np


class MainWindow():
    def __init__(self):
        self.sim: Simulator = None
        # Configure plotting
        plt.switch_backend('Qt5Agg')
        self.fig = plt.figure()
        self.grid = plt.GridSpec(2, 4)
        self.ax1 = plt.subplot(self.grid[:, :2], projection='3d')
        self.ax2 = plt.subplot(self.grid[0, 2:])
        self.ax3 = plt.subplot(self.grid[1, 2:])
        # Universe viewport configuration
        self.ax1._axes.set_aspect('equal')
        self.ax1.set_facecolor((24/255, 24/255, 24/255))
        self.ax1.axis('off')
        self.ax1.set_title("Universe viewport", y=1.085)

        # Hamiltonian viewport configuration
        self.ax2.set_title("Hamiltonian")
        self.ax2.set_xlim(0,100)
        hamilton_x_ticks = np.arange(0, 100, 5)
        self.ax2.set_xticks(hamilton_x_ticks)

        # Angular momentum viewport configuration
        self.ax3.set_title("Total angular momentum")

        # Start plot maximized
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()

    def __update(self, frame_n):
        self.ax1.title.set_text("Universe viewport epoch {}".format(frame_n))
        self.sim.run_step()
        self.scat._offsets3d = self.sim.get_pos()
        judgedMetrics = self.judger.judge()
        hamiltions = judgedMetrics['hanmiltonian']
        self.ax2.cla()
        self.ax2.set_title("Hamiltonian")
        self.ax2.plot(hamiltions)

        angularmomentum = judgedMetrics['angularMomentum']
        self.ax3.cla()
        self.ax3.set_title('Total angular momentum')
        self.ax3.plot(angularmomentum)
        
        #hamiltonian, angular_momentum = metrics(universe)

    def simulate(self, n_steps=100, n_stars=10):
        self.sim = SimRun(n_steps=n_steps, n_stars=n_stars)
        xs, ys, zs = self.sim.get_pos()
        self.judger = Judger(self.sim.universe)
        self.scat = self.ax1.scatter(xs, ys, zs, c='y')

        # Setup animation
        anim = FuncAnimation(self.fig, self.__update, interval=1)
        plt.show()

    def __update2(self, frame_n):
        self.ax1.title.set_text("Universe viewport epoch {}".format(frame_n))
        self.scat._offsets3d = self.sim.run_step()

    def replay(self, path):
        self.sim = Player(path)
        xs, ys, zs = self.sim.run_step()
        self.scat = self.ax1.scatter(xs, ys, zs, c='y')
        # Setup animation
        anim = FuncAnimation(self.fig, self.__update2, interval=50)
        plt.show()

