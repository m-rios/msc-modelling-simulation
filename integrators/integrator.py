
import sys
sys.path.append("..")
from abc import ABC, abstractmethod
from model.universe import Universe
from model.universe import Galaxy
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



class Leapfrog(Integrator):
    def __init__(self, dt:float=1e-5, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt)

    def do_step( self, uni: Universe):
        for i in range(len(uni.galaxy)):
            star = uni.galaxy[i]
            starhalfstep = star.pos + (timeStep * star.vel) / 2
            star.pos = starhalfstep
        
        for i in range(len(uni.galaxy)):
            n_acc = 0
            i_star = uni.galaxy[i]
            attracting_stars = self.selector.select(i, uni).galaxy
            for j_star in attracting_stars:
                d = i_star.pos - j_star.pos
                n_acc += cst.G * j_star.mass * d/norm(d)
            
            i_star.acc = n_acc
        

        for i in range(len(uni.galaxy)):
            star = uni.galaxy[i]
            star.vel = star.vel + timeStep * star.acc #get new vel
            star.pos = star.pos + timeStep * star.vel / 2    

class Hermite(Integrator):
    def __init__(self, dt:float=1e-5, selector:sel.Selector=sel.AllSelector):
        super().__init__(dt)
    
    def do_step(self, uni:Universe):

        shadowGalaxy = []
        shadowUniverse = Universe()
        shadowUniverse.galaxy = shadowGalaxy

        for i in range(len(uni.galaxy)): #calculate prediction velo and posiiton

            star = uni.galaxy[i]
            starJ = self.calculateJ(uni.galaxy)
            shadowStar = star()
            predicatPos = star.pos + star.vel * dt + star.vel * pow(dt, 2) / 2 + starJ * pow(dt, 3) / 6
            predicatVel = star.vel + star.acc * dt + starJ * pow(dt, 2) / 2
            shadowStar.pos = predicatPos
            shadowStar.vel = predicatVel
            shadowGalaxy.append(shadowStar)
        

        for i in range(len(shadowUniverse.galaxy)): #calculate prediction acceleration

            i_star = shadowUniverse.galaxy[i]
            predicateAcc = 0

            attracting_stars = self.selector.select(i, shadowUniverse).galaxy
            for j_star in attracting_stars:
                d = i_star.pos - j_star.pos
                predicateAcc += cst.G * j_star.mass * d/norm(d)
            
            i_star.acc = predicateAcc
        
        for i in range(len(uni.galaxy)):
            i_star = uni.galaxy[i]
            i_star_jerk = self.calculateJ(uni.galaxy, i)
            
            i_shadowStar = shadowGalaxy[i]
            i_shadowStar_jerk = self.calculateJ(shadowGalaxy, i)


            i_star_v1 = i_star.vel + (i_star.acc + i_shadowStar.acc) * dt / 2 + (i_star_jerk - i_shadowStar_jerk) * pow(dt, 2) / 12
            i_star.pos = i_star.pos + (i_star.vel + i_star_v1) * dt / 2 + (i_star.acc - i_shadowStar.acc) * pow(dt, 2) / 12
            i_star.vel = i_star_v1

    
    def calculateJ(galaxy:Galaxy, i:int=1):

        i_star = galaxy[i]
        jerk = 0
        attracting_stars = self.selector.select(i, uni).galaxy
        for j_star in attracting_stars:
            d = i_star.pos - j_star.pos
            relativeV = i_star.vel - j_star.vel
            jerk += cst.G * j_star.mass * (relativeV/pow(norm(relativeV,3)) - 3 * (d * relativeV) * d / pow(norm(d), 5))
        
        return jerk

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
