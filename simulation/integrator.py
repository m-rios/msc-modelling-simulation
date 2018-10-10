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

    def do_step2(self, uni: Universe):
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

    def do_step(self, uni: Universe):
        assert isinstance(uni, Universe)
        acc = np.zeros((len(uni), 3))
        for i in range(len(uni)):
            attractors = uni[self.selector.select(i, uni)]
            i_star = uni[i]
            for j_star in attractors:
                d = j_star['pos'] - i_star['pos']
                acc[i,:] = acc[i,:] + j_star['mass'] * d/(np.linalg.norm(d)**3)
        acc = cst.G * acc
        uni['vel'] = uni['vel'] + self.dt*acc
        uni['pos'] = uni['pos'] + self.dt*uni['vel']

class Leapfrog(Integrator):
    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)
    
    def do_step( self, uni: Universe):

        assert isinstance(uni, Universe)
        for i in range(len(uni)):
            star = uni.stars[i]
            starhalfstep = star['pos'] + (self.dt * star['vel']) / 2
            star['pos'] = starhalfstep
        
        for i in range(len(uni)):
            n_acc = 0
            i_star = uni.stars[i]
            attracting_stars = uni[self.selector.select(i, uni)]
            for j_star in attracting_stars:
                d = i_star['pos'] - j_star['pos']
                n_acc += cst.G * j_star['mass'] * d/norm(d)
            
            i_star['acc'] = n_acc
        

        for i in range(len(uni)):
            star = uni.stars[i]
            star['vel'] = star['vel'] + self.dt * star['acc'] #get new vel
            star['pos'] = star['pos'] + self.dt * star['vel'] / 2
    

class Hermite(Integrator):
    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)
    
    def do_step(self, uni:Universe):

        shadowUniverse = Universe(n_stars=len(uni))

        for i in range(len(uni)): #calculate prediction velo and posiiton

            star = uni.stars[i]
            starJerk = self.calculateJ(uni, i)
            shadowStar = shadowUniverse.stars[i]
            predicatPos = star['pos'] + star['vel'] * self.dt + star['vel'] * pow(self.dt, 2) / 2 + starJerk * pow(self.dt, 3) / 6
            predicatVel = star['vel'] + star['acc'] * self.dt + starJerk * pow(self.dt, 2) / 2
            shadowStar['pos'] = predicatPos
            shadowStar['vel'] = predicatVel
        

        for i in range(len(shadowUniverse)): #calculate prediction acceleration

            i_star = shadowUniverse.stars[i]
            predicateAcc = 0

            attracting_stars = shadowUniverse[self.selector.select(i, shadowUniverse)]
            for j_star in attracting_stars:
                d = i_star['pos'] - j_star['pos']
                predicateAcc += cst.G * j_star['mass'] * d/norm(d)
            
            i_star['acc'] = predicateAcc
        
        for i in range(len(uni)):
            i_star = uni.stars[i]
            i_star_jerk = self.calculateJ(uni, i)
            
            i_shadowStar = shadowUniverse.stars[i]
            i_shadowStar_jerk = self.calculateJ(shadowUniverse, i)


            i_star_v1 = i_star['vel'] + (i_star['acc'] + i_shadowStar['acc']) * self.dt / 2 + (i_star_jerk - i_shadowStar_jerk) * pow(self.dt, 2) / 12
            i_star['pos'] = i_star['pos'] + (i_star['vel'] + i_star_v1) * self.dt / 2 + (i_star['acc'] - i_shadowStar['acc']) * pow(self.dt, 2) / 12
            i_star['vel'] = i_star_v1

    
    def calculateJ(self,uni:Universe, i:int=1):

        i_star = uni.stars[i]
        jerk = 0
        attracting_stars = uni[self.selector.select(i, uni)]
        for j_star in attracting_stars:
            d = i_star['pos'] - j_star['pos']
            relativeV = i_star['vel'] - j_star['vel']
            jerk += cst.G * j_star['mass'] * (relativeV/pow(norm(relativeV), 3) - 3 * (d * relativeV) * d / pow(norm(d), 5))
        
        return jerk


if __name__ == '__main__':
    # import timeit
    # i2 = Euler()
    # u2 = Universe()
    # stars = np.copy(u2.stars)
    # print(timeit.timeit('i2.do_step(u2)', 'from __main__ import i2, u2', number=10))
    # u2.stars = stars
    # print(timeit.timeit('i2.do_step2(u2)', 'from __main__ import i2, u2', number=10))

    it = Euler()
    u = Universe()
    stars_original = np.copy(u.stars)
    it.do_step(u)
    stars_fast = np.copy(u.stars)
    u.stars = stars_original
    it.do_step2(u)
    stars_slow = u.stars
    print(np.array_equal(stars_fast, stars_slow))
