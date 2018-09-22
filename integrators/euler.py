from integrators.integrator import Integrator
from integrators.selector import Selector
from integrators.allselector import AllSelector
from model.universe import Universe
from numpy.linalg import norm
from model import *  # import constants


class Euler(Integrator):
    def __init__(self, selector: Selector = AllSelector()):
        assert isinstance(selector, Selector)
        self.dt = 1e-5
        self.selector = selector

    def do_step(self, uni: Universe):
        assert isinstance(uni, Universe)

        # Compute acceleration for each star in the universe
        for i in range(uni.n_stars):
            attracting_stars = self.selector.select(i, uni).stars
            i_star = uni.stars[i]
            n_acc = 0

            for j_star in attracting_stars:
                d = j_star.pos - i_star.pos
                n_acc += G * j_star.mass * d/norm(d)

            # Integrate acceleration and update new values
            n_vel = i_star.vel + self.dt*n_acc
            n_pos = i_star.pos + self.dt*n_vel

            uni.stars[i].acc = n_acc
            uni.stars[i].vel = n_vel
            uni.stars[i].pos = n_pos
