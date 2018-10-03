import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Don't remove, needed for the 3d plot
from matplotlib.animation import FuncAnimation
from simulation import SimRun


class MainWindow():
    def __init__(self, n_stars):
        self.sim = SimRun(n_stars=n_stars)

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
        # ax1.grid(False)
        self.ax1.axis('off')
        self.ax1.set_title("Universe viewport", y=1.085)
        xs, ys, zs = self.sim.get_pos()
        self.scat = self.ax1.scatter(xs, ys, zs, c='y')

        # Hamiltonian viewport configuration
        self.ax2.set_title("Hamiltonian")

        # Angular momentum viewport configuration
        self.ax3.set_title("Total angular momentum")

        # Setup animation
        self.anim = FuncAnimation(self.fig, self.update, interval=1)

        # Start plot maximized
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

    def update(self, frame_n):
        self.ax1.title.set_text("Universe viewport epoch {}".format(frame_n))
        self.sim.run_step()
        self.scat._offsets3d = self.sim.get_pos()

    def plot_metrics(self):
        pass


