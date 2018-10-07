from abc import ABC, abstractmethod
from model.universe import Universe
import model.constants as cst
from numpy.linalg import norm
import simulation.selector as sel
import numpy as np

class Integrator(ABC):
    # Abstract integrator class. All integrator methods must extend this class

    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        assert isinstance(selector, sel.Selector) and isinstance(dt, float)
        self.dt = dt
        self.selector = selector

    @abstractmethod
    def do_step(self, universe: Universe):
        raise NotImplemented


class Euler(Integrator):
    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)

    def do_step(self, uni: Universe):
        assert isinstance(uni, Universe)

        # Compute acceleration for each star in the universe
        for i in range(len(uni)):
            attractors = uni[self.selector.select(i, uni)]
            i_star = np.repeat(uni[i], len(uni) - 1, axis=0)

            d = attractors['pos'] - i_star['pos']
            d = d/(norm(d, axis=0)**3)
            acc = np.multiply(d, np.repeat(attractors['mass'], 3).reshape(len(attractors),3))
            n_acc = np.sum(acc, axis=0)*cst.G

            # Integrate acceleration and update new values
            n_vel = uni[i]['vel'] + self.dt*n_acc
            n_pos = uni[i]['pos'] + self.dt*n_vel

            uni[i]['acc'] = n_acc
            uni[i]['vel'] = n_vel
            uni[i]['pos'] = n_pos


if __name__ == '__main__':
    import timeit
    i2 = Euler()
    u2 = Universe()
    print(timeit.timeit('i2.do_step(u2)', 'from __main__ import i2, u2', number=10))