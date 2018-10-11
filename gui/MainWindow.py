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
        # self.ax1.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

        # self.ax1.axis('off')
        self.ax1.set_title("Universe viewport", y=1.085)
        xs, ys, zs = self.sim.get_pos()
        self.stars, = self.ax1.plot(xs, ys, zs, 'oy', markersize=2)
        self.x, = self.ax1.plot([0, 1], [0, 0], [0, 0], color='red')
        self.y, = self.ax1.plot([0, 0], [0, 1], [0, 0], color='green')
        self.z, = self.ax1.plot([0, 0], [0, 0], [0, 1], color='blue')
        # self.stars, = self.ax1.plot(xs, ys, 'oy')

        # Hamiltonian viewport configuration
        self.ax2.set_title("Hamiltonian")
        self.ax2.set_xlim(0,100)
        # hamil, A = self.judger.metrics(self.sim.universe)
        # self.hamiltonian_plot, = self.ax2.plot(hamil['H'], [0])

        # Angular momentum viewport configuration
        self.ax3.set_title("Total angular momentum")
        # self.angularmomentum = self.ax3.plot(metrics['angularMomentum'])

        # Start plot maximized
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()

    def __update(self, frame_n):
        # universe
        self.ax1.title.set_text("Universe viewport epoch {}".format(self.sim.epoch))
        self.sim.run_step()
        xs, ys, zs = self.sim.get_pos()
        self.stars.set_data([xs, ys])
        self.stars.set_3d_properties(zs)
        # self.x.set_3d_properties([0, 0])
        # self.y.set_3d_properties([0, 0])
        # self.z.set_3d_properties([0, 1])
        # metrics
        # hamil, A = self.judger.metrics(self.sim.universe)
        # self.hamiltonian_plot.set_data(hamil['H'], np.arange(0, len(hamil['H'])))
        # self.hamiltonian_plot.axes.axis([0, len(hamil['H']), np.min(hamil['H']), np.max(hamil['H'])])
        return self.stars,
        # return self.stars, self.hamiltonian_plot
        # return self.hamiltonian_plot,

    def __init(self):
        xs, ys, zs = self.sim.get_pos()
        self.stars.set_data([xs, ys])
        self.stars.set_3d_properties(zs)
        # self.x.set_3d_properties([0, 0])
        # self.y.set_3d_properties([0, 0])
        # self.z.set_3d_properties([0, 1])

        # hamil, _ = self.judger.metrics(self.sim.universe)
        # self.hamiltonian_plot.set_data(hamil['H'], [0])
        # self.hamiltonian_plot.axes.axis([0, len(hamil['H']), np.min(hamil['H']), np.max(hamil['H'])])
        return self.stars,
        # return self.stars, self.hamiltonian_plot
        # return self.hamiltonian_plot,

    def simulate(self):
        # xs, ys, zs = self.sim.get_pos()
        # self.scat = self.ax1.scatter(xs, ys, zs, c='y')

        # Setup animation
        anim = FuncAnimation(self.fig, self.__update, interval=50,init_func=self.__init, blit=True)
        plt.show()


