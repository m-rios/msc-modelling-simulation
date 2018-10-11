import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Don't remove, needed for the 3d plot
from matplotlib.animation import FuncAnimation
from simulation import Simulator
from model.galaxyMetrics import Judger
import numpy as np


class MainWindow:
    def __init__(self, sim: Simulator):
        self.sim = sim
        self.judger = Judger(self.sim.universe)
        # Configure plotting
        plt.switch_backend('Qt5Agg')
        self.fig = plt.figure()
        self.grid = plt.GridSpec(2, 4)
        self.ax1 = plt.subplot(self.grid[:, :2], projection='3d')
        self.ax2 = plt.subplot(self.grid[0, 2:])
        self.ax3 = plt.subplot(self.grid[1, 2:])

        # Universe viewport configuration
        # self.ax1._axes.set_aspect('equal')
        self.ax1.set_facecolor((24/255, 24/255, 24/255))
        self.ax1.axis('off')
        self.ax1.set_title("Universe viewport", y=1.085)
        xs, ys, zs = self.sim.get_pos()
        self.stars, = self.ax1.plot(xs, ys, zs, 'oy', markersize=2)
        # self.stars, = self.ax1.plot(xs, ys, 'oy')

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

    def __plot_metrics(self):
        metrics = self.judger.metrics(self.sim.universe)
        hamiltions = metrics['hanmiltonian']
        self.ax2.cla()
        self.ax2.set_title("Hamiltonian")
        potential = hamiltions['potential']
        kinetic = hamiltions['kinetic']
        HSum = hamiltions['sum']
        # self.ax2.plot(potential, color='red', label='potential')
        # self.ax2.plot(kinetic, color='green', label='kinetic')
        self.ax2.plot(HSum, color='blue', label='HSum')
        # self.ax2.plot(hamiltions)

        angularmomentum = metrics['angularMomentum']
        self.ax3.cla()
        self.ax3.set_title('Total angular momentum')
        self.ax3.plot(angularmomentum, color='red', label='x angular momentum')

        #hamiltonian, angular_momentum = metrics(universe)

    def __update(self, frame_n):
        self.ax1.title.set_text("Universe viewport epoch {}".format(self.sim.epoch))
        self.sim.run_step()
        xs, ys, zs = self.sim.get_pos()
        self.stars.set_data([xs, ys])
        self.stars.set_3d_properties(zs)
        return self.stars,

    def __init(self):
        xs, ys, zs = self.sim.get_pos()
        self.stars.set_data([xs, ys])
        self.stars.set_3d_properties(zs)
        return self.stars,

    def simulate(self):
        # xs, ys, zs = self.sim.get_pos()
        # self.scat = self.ax1.scatter(xs, ys, zs, c='y')

        # Setup animation
        anim = FuncAnimation(self.fig, self.__update, interval=50,init_func=self.__init, blit=True)
        plt.show()


