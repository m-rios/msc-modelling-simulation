from . import Universe
from . import constants 
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from numpy.linalg import norm
#envtrul

class Jugde:
    def __init__(self):
        self.hamiltonians = []
        self.angular_momentums = []

    def judge(self, u: Universe):
        # print('start!')
        angular_momentum_sum = 0
        potential_energy_sum = 0
        kinetic_energy_sum = 0
        for i in range(len(u)):
            current_star = u[i]
            pos = current_star['pos']
            mass = current_star['mass']
            vel = current_star['vel']
            kinetic_energy = pow(norm(vel),2)/(2 * mass)
            kinetic_energy_sum += kinetic_energy

            momentum = mass * vel
            angular_momentum = np.linalg.norm(np.cross(pos, momentum))
            angular_momentum_sum += angular_momentum

            for j in range(len(u)):
                jStar = u[j]
                jPos = jStar['pos']
                jMass = jStar['mass']

                if i != j:
                    U = constants.G * mass * jMass / norm(pos - jPos)
                    potential_energy_sum += U

        H = kinetic_energy_sum + potential_energy_sum

        self.hamiltonians.append(H)
        self.angular_momentums.append(angular_momentum_sum)
        return self.hamiltonians, self.angular_momentums




