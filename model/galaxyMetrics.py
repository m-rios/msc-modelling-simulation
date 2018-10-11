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


class Judger:
    """docstring for Judger"""
    def __init__(self, judgedUniverse: Universe=None):
        super(Judger, self).__init__()
        self.judgedUniverse=judgedUniverse
        self.hamiltionians = {'potential' : [], 'kinetic':[], 'sum' : []}
        self.angularMomentSums = []

    def metrics(self, u: Universe):
        # u = self.judgedUniverse
        U = 0 # Potential energy
        T = 0 # Kinetic energy
        L = np.zeros(3)
        for i_idx in range(len(u)):
            i = u[i_idx]
            p = i['mass']*i['vel'] # linear momentum
            T += (norm(p)**2)/(2*i['mass'])
            L += np.cross(i['pos'], p)
            for j_idx in range(len(u)):
                if i_idx == j_idx:
                    continue
                j = u[j_idx]
                U -= constants.G*(i['mass']*j['mass'])/norm(j['pos']-i['pos'])
        H = U + T
        self.angularMomentSums.append(norm(L))
        self.hamiltionians['potential'].append(U)
        self.hamiltionians['kinetic'].append(T)
        self.hamiltionians['sum'].append(H)
        return {'hanmiltonian' : self.hamiltionians, 'angularMomentum' : self.angularMomentSums}


    def judge(self, u: Universe):
        self.judgedUniverse = u
        # print('start!')
        potentilEnergySum = 0
        kineticEnergySum = 0
        angularMomentumSum = [0,0,0]

        for i in range(len(self.judgedUniverse.stars)):
            currentStart = self.judgedUniverse.stars[i]
            pos = currentStart['pos']
            mass = currentStart['mass']
            vel = currentStart['vel']

            momentum = mass * vel
            kineticEnergy = np.dot(momentum, momentum)/(2 * mass)
            kineticEnergySum += kineticEnergy


            angularMomentum = np.cross(pos, momentum)
            angularMomentumSum += angularMomentum

            for j in range(len(self.judgedUniverse.stars)):
                jStar = self.judgedUniverse.stars[j]
                jPos = jStar['pos']
                jMass = jStar['mass']

                if i != j:
                    U = constants.G * mass * jMass / norm(jPos - pos)
                    potentilEnergySum -= U

        # self.hamiltionians.append(H)
        potential = self.hamiltionians['potential']
        potential.append(potentilEnergySum)
        kinetic = self.hamiltionians['kinetic']
        kinetic.append(kineticEnergySum)
        HEnergy = self.hamiltionians['sum']
        HEnergy.append(potentilEnergySum + kineticEnergySum)


        # xes = self.angularMomentSums['xes']
        # xes.append(angularMomentumSum[0])
        # ys = self.angularMomentSums['ys']
        # ys.append(angularMomentumSum[1])
        # zes = self.angularMomentSums['zes']
        # zes.append(angularMomentumSum[2]
        self.angularMomentSums.append(norm(angularMomentumSum))
        return {'hanmiltonian' : self.hamiltionians, 'angularMomentum' : self.angularMomentSums}


    def judge2(self, u: Universe):
        # print('start!')
        angularMomentumSum = [0,0,0]

        for i in range(len(u)):
            currentStart =  u[i]
            pos = currentStart['pos']
            mass = currentStart['mass']
            vel = currentStart['vel']

            momentum = vel * mass
            angularMomentum = np.cross(pos, momentum)
            angularMomentumSum += angularMomentum

        self.angularMomentSums.append(norm(angularMomentumSum))
        print(norm(angularMomentumSum))
        return {'hanmiltonian' : self.hamiltionians, 'angularMomentum' : self.angularMomentSums}


