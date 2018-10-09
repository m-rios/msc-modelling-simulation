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


class Leapfrog(Integrator):
    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)
    
    def do_step( self, uni: Universe):

        assert isinstance(uni, Universe)
        for i in range(len(uni)):
            star = uni.stars[i]
            starhalfstep = star['pos'] + (timeStep * star['vel']) / 2
            star['pos'] = starhalfstep
        
        for i in range(len(uni.galaxy)):
            n_acc = 0
            i_star = uni.stars[i]
            attracting_stars = uni[self.selector.select(i, uni)]
            for j_star in attracting_stars:
                d = i_star['pos'] - j_star['pos']
                n_acc += cst.G * j_star['mass'] * d/norm(d)
            
            i_star.acc = n_acc
        

        for i in range(len(uni)):
            star = uni.stars[i]
            star['vel'] = star['vel'] + timeStep * star['acc'] #get new vel
            star['pos'] = star['pos'] + timeStep * star['vel'] / 2
    

class Hermite(Integrator):
    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)
    
    # def do_step(self, uni:Universe):

    #     shadowGalaxy = []
    #     shadowUniverse = Universe()
    #     shadowUniverse.galaxy = shadowGalaxy

    #     for i in range(len(uni)): #calculate prediction velo and posiiton

    #         star = uni.stars[i]
    #         starJ = self.calculateJ(uni, i)
    #         shadowStar = [('pos', (np.float64, 3)),
    #                                           ('vel', (np.float64, 3)),
    #                                           ('acc', (np.float64, 3)),
    #                                           ('acc2', (np.float64, 3)),
    #                                           ('acc3', (np.float64, 3)),
    #                                           ('mass', np.float64)]
    #         predicatPos = star['pos'] + star['vel'] * dt + star['vel'] * pow(dt, 2) / 2 + starJ * pow(dt, 3) / 6
    #         predicatVel = star['vel'] + star['acc'] * dt + starJ * pow(dt, 2) / 2
    #         shadowStar['pos'] = predicatPos
    #         shadowStar['vel'] = predicatVel
    #         shadowGalaxy.append(shadowStar)
        

    #     for i in range(len(shadowUniverse.galaxy)): #calculate prediction acceleration

    #         i_star = shadowUniverse.galaxy[i]
    #         predicateAcc = 0

    #         attracting_stars = self.selector.select(i, shadowUniverse).galaxy
    #         for j_star in attracting_stars:
    #             d = i_star.pos - j_star.pos
    #             predicateAcc += cst.G * j_star.mass * d/norm(d)
            
    #         i_star.acc = predicateAcc
        
    #     for i in range(len(uni.galaxy)):
    #         i_star = uni.galaxy[i]
    #         i_star_jerk = self.calculateJ(uni.galaxy, i)
            
    #         i_shadowStar = shadowGalaxy[i]
    #         i_shadowStar_jerk = self.calculateJ(shadowGalaxy, i)


    #         i_star_v1 = i_star.vel + (i_star.acc + i_shadowStar.acc) * dt / 2 + (i_star_jerk - i_shadowStar_jerk) * pow(dt, 2) / 12
    #         i_star.pos = i_star.pos + (i_star.vel + i_star_v1) * dt / 2 + (i_star.acc - i_shadowStar.acc) * pow(dt, 2) / 12
    #         i_star.vel = i_star_v1

    
    # def calculateJ(uni:Universe, i:int=1):

    #     i_star = uni.stars[i]
    #     jerk = 0
    #     attracting_stars = uni[self.selector.select(i, uni)]
    #     for j_star in attracting_stars:
    #         d = i_star['pos'] - j_star['pos']
    #         relativeV = i_star['vel'] - j_star['vel']
    #         jerk += cst.G * j_star['mass'] * (relativeV/pow(norm(relativeV,3)) - 3 * (d * relativeV) * d / pow(norm(d), 5))
        
    #     return jerk


if __name__ == '__main__':
    import timeit
    i2 = Euler()
    u2 = Universe()
    print(timeit.timeit('i2.do_step(u2)', 'from __main__ import i2, u2', number=10))
