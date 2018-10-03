from abc import ABC, abstractmethod
from model.universe import Universe
import model.constants as cst
from numpy.linalg import norm
import integrators.selector as sel
from datetime import datetime
import config
import os
import numpy as np

class Integrator(ABC):
    # Abstract integrator class. All integrator methods must extend this class

    def __init__(self, dt: float = 1e-5, selector: sel.Selector = sel.AllSelector()):
        assert isinstance(selector, sel.Selector) and isinstance(dt, float)
        self.dt = dt
        self.selector = selector

    @abstractmethod
    def do_step(self, universe: Universe):
        raise NotImplemented


class Euler(Integrator):
    def __init__(self, dt: float = 1e-5, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)

    def do_step(self, uni: Universe):
        assert isinstance(uni, Universe)

        # Compute acceleration for each star in the universe
        for i in range(len(uni.galaxy)):
            attracting_stars = self.selector.select(i, uni).galaxy
            i_star = uni.galaxy[i]
            n_acc = 0

            for j_star in attracting_stars:
                d = j_star.pos - i_star.pos
                n_acc += cst.G * j_star.mass * d/norm(d)

            # Integrate acceleration and update new values
            n_vel = i_star.vel + self.dt*n_acc
            n_pos = i_star.pos + self.dt*n_vel

            uni.stars[i].acc = n_acc
            uni.stars[i].vel = n_vel
            uni.stars[i].pos = n_pos

            

class leapfrot(Integrator):
    def __init__(self, dt:float=1e-5):
        super().__init__(dt)
    
    def do_step(self, uni: Universe):
        for star in calculatedUniverse.n_stars:
            starhalfstep = star.pos + (timeStep * star.vel) / 2 # 
            star.pos = starhalfstep
        for star in calculatedUniverse.n_stars:
            star.acc = calculatedUniverse.getAccelerationOnStar(star) # new acceleration
        
        for star in calculatedUniverse.n_stars:
            star.vel = star.vel + timeStep * star.acc #get new vel
            star.pos = star.pos + timeStep * star.vel / 2


class SimRun:
    def __init__(self, n_steps: int = 10**10, n_stars: int = 10, universe: Universe = None, integrator: Integrator = Euler(), name: str = ""):
        assert isinstance(n_steps, int) and isinstance(integrator, Integrator) and isinstance(name, str)

        self.n_steps = n_steps
        self.epoch = 0
        self.integrator = integrator

        if universe is None:
            self.universe = Universe(n_stars=n_stars)
        else:
            assert isinstance(universe, Universe)
            self.universe = universe

        if name == "":
            self.name = "{} {} {}".format(datetime.now(), self.n_steps, type(self.integrator).__name__.lower())
        else:
            self.name = name

        self.log_file_path = os.path.join(config.log_dir, 'test-'+self.name+'.log')
        self.logfile = open(self.log_file_path, 'x')
        self.simlog = ""

    def _save(self):
        self.logfile.write(self.simlog)
        self.simlog = ""
        self.logfile.flush()

    def run(self):
        # Initialize log file
        while self.run():
            pass

    def run_step(self):
        self.simlog += "e:{},{}\n".format(self.epoch, str(self.universe.galaxy))
        self.integrator.do_step(self.universe)
        if self.epoch % 1000 == 0:
            self._save()
        self.epoch += 1
        return self.epoch < self.n_steps

    def _get_dim(self, dim: int = 0):
        getd = np.vectorize(lambda star: star.pos[dim])
        return getd(self.universe.galaxy)

    def xs(self):
        return self._get_dim(0)

    def ys(self):
        return self._get_dim(1)

    def zs(self):
        return self._get_dim(2)

    def get_pos(self):
        return (self.xs(), self.ys(), self.zs())

    def __delete__(self, instance):
        self.logfile.flush()
        self.logfile.close()


if __name__ == '__main__':
    r = SimRun(n_steps=5)
    r.run()
