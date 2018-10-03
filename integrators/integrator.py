from abc import ABC, abstractmethod
from model.universe import Universe
import model.constants as cst
from numpy.linalg import norm
import integrators.selector as sel


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
        for i in range(uni.n_stars):
            attracting_stars = self.selector.select(i, uni).stars
            i_star = uni.stars[i]
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