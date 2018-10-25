from abc import ABC, abstractmethod
from model.universe import Universe
import model.constants as cst
from numpy.linalg import norm
import simulation.selector as sel
import numpy as np
import copy


class Integrator(ABC):
    # Abstract integrator class. All integrator methods must extend this class

    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        assert isinstance(selector, sel.Selector) and isinstance(dt, float)
        self.dt = dt
        self.selector = selector
        self.name = ''

    def acceleration(self, uni: Universe):
        acc = np.zeros((len(uni), 3))
        for i in range(len(uni)):
            attractors = uni[self.selector.select(i, uni)]
            i_star = uni[i]
            # Compute accelerations
            for j_star in attractors:
                d = j_star['pos'] - i_star['pos']
                acc[i, :] = acc[i, :] + j_star['mass'] * d / (np.linalg.norm(d) ** 3)
        acc = cst.G * acc
        return acc

    @abstractmethod
    def do_step(self, universe: Universe):
        raise NotImplemented


class Euler(Integrator):
    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)
        self.name = 'euler'

    def do_step(self, uni: Universe):
        assert isinstance(uni, Universe)
        n_acc = self.acceleration(uni)
        uni['vel'] = uni['vel'] + uni['acc'] * self.dt
        uni['pos'] = uni['pos'] + uni['vel'] * self.dt
        uni['acc'] = n_acc  # Update new acceleration


class Leapfrog(Integrator):
    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)
        print("Created Leapfrog Integrator")
        self.name = 'leapfrog'

    def do_step(self, uni: Universe):
        assert isinstance(uni, Universe)
        n_acc = self.acceleration(uni)
        # Update positions
        uni['pos'] = uni['pos'] + uni['vel']*self.dt + 1/2 * (uni['acc']*self.dt**2)
        uni['vel'] = uni['vel'] + 1/2 * (uni['acc'] + n_acc) * self.dt
        uni['acc'] = n_acc


class Hermite(Integrator):
    __shadowUniverse = Universe(10)
    def __init__(self, dt: float = 1e-3, selector: sel.Selector = sel.AllSelector()):
        super().__init__(dt, selector)
        self.name = 'hermite'
        self.__shadowUniverse = Universe(10)

    def do_step(self, uni:Universe):
        # old_pos = @pos  //(1)
        # old_vel = @vel
        # old_acc = acc
        # old_jerk = jerk

        # @pos += @vel*dt + old_acc*(dt*dt/2.0) + old_jerk*(dt*dt*dt/6.0) //(2) (3)
        # @vel += old_acc*dt + old_jerk*(dt*dt/2.0)

        

        #recorde all the all values (1)
        self.__shadowUniverse = Universe(len(uni))
        old_jerks = []
        for i in range(len(uni)):
            old_jerk = self.calculateJ(uni, i)
            old_jerks.append(old_jerk)
            i_star = uni.stars[i]
            shadowStar = self.__shadowUniverse.stars[i]
            shadowStar['pos'] = copy.deepcopy(i_star['pos'])
            shadowStar['vel'] = copy.deepcopy(i_star['vel'])
            shadowStar['acc'] = copy.deepcopy(i_star['acc']) 
        
        #calculate the middle status (2)
        
        for i in range(len(self.__shadowUniverse)):
            i_star = uni.stars[i]
            i_shadow_star = self.__shadowUniverse.stars[i]
            i_shadow_star_jerk = old_jerks[i]
            i_star['pos'] += i_shadow_star['vel'] * self.dt + i_shadow_star['acc'] * (pow(self.dt,2) / 2.0) + i_shadow_star_jerk * (pow(self.dt, 3) / 6.0)
            i_star['vel'] += i_shadow_star['acc'] * self.dt + i_shadow_star_jerk * (pow(self.dt, 2) / 2.0) 

        #calculate a new acceleration and jerk (3)
        new_jerks = []
        for i in range(len(uni)):
            n_acc = 0
            i_star = uni.stars[i]
            jerk = self.calculateJ(uni, i)
            new_jerks.append(jerk)
            attracting_stars = uni[self.selector.select(i, uni)]
            for j_star in attracting_stars:
                d = i_star['pos'] - j_star['pos']
                n_acc += cst.G * j_star['mass'] * d/(norm(d)**3)
            
            i_star['acc'] = n_acc
        
        # @vel = old_vel + (old_acc + acc)*(dt/2.0) + (old_jerk - jerk)*(dt*dt/12.0) //(4)
        # @pos = old_pos + (old_vel + vel)*(dt/2.0) + (old_acc - acc)*(dt*dt/12.0)

        #calculate the final result (4)
        for i in range(len(uni)):
            i_star = uni.stars[i]
            i_shadow_star = self.__shadowUniverse.stars[i]
            old_jerk = old_jerks[i]
            jerk = new_jerks[i]
            i_star['vel'] = i_shadow_star['vel'] + (i_shadow_star['acc'] + i_star['acc']) * (self.dt / 2.0) + (old_jerk - jerk) * (pow(self.dt,2) / 12.0)
            i_star['pos'] = i_shadow_star['pos'] + (i_shadow_star['vel'] + i_star['vel']) * (self.dt / 2.0) + (i_shadow_star['acc'] - i_star['acc']) * (pow(self.dt,2) / 12.0)
            
    
    
    def calculateJ(self,uni:Universe, i:int=1):

        i_star = uni.stars[i]
        jerk = 0
        attracting_stars = uni[self.selector.select(i, uni)]
        for j_star in attracting_stars:
            d = i_star['pos'] - j_star['pos']
            relativeV = i_star['vel'] - j_star['vel']
            jerk += cst.G * j_star['mass'] * (relativeV/pow(norm(d), 3) - 3 * (norm(d) * relativeV) * norm(d) / pow(norm(d), 5))
    
        return jerk
    # def do_step(self, uni:Universe):

    #     shadowUniverse = Universe(n_stars=len(uni))

    #     for i in range(len(uni)): #calculate prediction velo and posiiton

    #         star = uni.stars[i]
    #         starJerk = self.calculateJ(uni, i)
    #         shadowStar = shadowUniverse.stars[i]
    #         predicatPos = star['pos'] + star['vel'] * self.dt + star['vel'] * pow(self.dt, 2) / 2 + starJerk * pow(self.dt, 3) / 6
    #         predicatVel = star['vel'] + star['acc'] * self.dt + starJerk * pow(self.dt, 2) / 2
    #         shadowStar['pos'] = predicatPos
    #         shadowStar['vel'] = predicatVel
        

    #     for i in range(len(shadowUniverse)): #calculate prediction acceleration

    #         i_star = shadowUniverse.stars[i]
    #         predicateAcc = 0

    #         attracting_stars = shadowUniverse[self.selector.select(i, shadowUniverse)]
    #         for j_star in attracting_stars:
    #             d = i_star['pos'] - j_star['pos']
    #             predicateAcc += cst.G * j_star['mass'] * d/norm(d)
            
    #         i_star['acc'] = predicateAcc
        
    #     for i in range(len(uni)):
    #         i_star = uni.stars[i]
    #         i_star_jerk = self.calculateJ(uni, i)
            
    #         i_shadowStar = shadowUniverse.stars[i]
    #         i_shadowStar_jerk = self.calculateJ(shadowUniverse, i)


    #         i_star_v1 = i_star['vel'] + (i_star['acc'] + i_shadowStar['acc']) * self.dt / 2 + (i_star_jerk - i_shadowStar_jerk) * pow(self.dt, 2) / 12
    #         i_star['pos'] = i_star['pos'] + (i_star['vel'] + i_star_v1) * self.dt / 2 + (i_star['acc'] - i_shadowStar['acc']) * pow(self.dt, 2) / 12
    #         i_star['vel'] = i_star_v1

    
    


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
