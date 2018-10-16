from . import Universe
from . import constants 
import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import squareform, pdist


class Judger:
    """docstring for Judger"""
    def __init__(self, judgedUniverse: Universe=None):
        self.judgedUniverse = judgedUniverse
        self.hamiltonians = {'U': [], 'T': [], 'H': []}
        self.angular_moms = []
        self.min_distances = []

    def metrics(self, u: Universe):
        # u = self.judgedUniverse
        U = 0  # Potential energy
        T = 0  # Kinetic energy
        L = np.zeros(3)
        for i_idx in range(len(u)):
            i = u[i_idx]
            p = i['mass']*i['vel']  # linear momentum
            T += (norm(p)**2)/(2*i['mass'])
            L += np.cross(i['pos'], p)
            for j_idx in range(len(u)):
                if i_idx == j_idx:
                    continue
                j = u[j_idx]
                U -= constants.G*(i['mass']*j['mass'])/norm(j['pos']-i['pos'])
        H = U + T
        self.angular_moms.append(norm(L))
        self.hamiltonians['U'].append(U)
        self.hamiltonians['T'].append(T)
        self.hamiltonians['H'].append(H)
        return self.hamiltonians, self.angular_moms

    def min_dist(self, u: Universe):
        d = np.min(pdist(u['pos']))
        self.min_distances.append(d)
        return self.min_distances
