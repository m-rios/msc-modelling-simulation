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
		

	def judge(self):
		# print('start!')
		potentilEnergySum = 0
		kineticEnergySum = 0
		angularMomentumSum = [0,0,0]

		for i in range(len(self.judgedUniverse.stars)):
			currentStart = self.judgedUniverse.stars[i]
			pos = currentStart['pos']
			mass = currentStart['mass']
			vel = currentStart['vel']
			kineticEnergy = np.dot(vel, vel)/(2 * mass) 
			kineticEnergySum += kineticEnergy

			momentum = vel * mass
			angularMomentum = np.cross(pos, momentum)
			angularMomentumSum += angularMomentum

			for j in range(len(self.judgedUniverse.stars)):
				jStar = self.judgedUniverse.stars[j]
				jPos = jStar['pos']
				jMass = jStar['mass']

				if i != j:
					U = constants.G * mass * jMass / norm(pos - jPos)
					potentilEnergySum -= U
		
		# self.hamiltionians.append(H)
		potential = self.hamiltionians['potential']
		potential.append(potentilEnergySum)
		kinetic = self.hamiltionians['kinetic']
		kinetic.append(kineticEnergySum)
		print (kineticEnergySum)
		HEnergy = self.hamiltionians['sum']
		HEnergy.append(potentilEnergySum + kineticEnergySum)


		# xes = self.angularMomentSums['xes']
		# xes.append(angularMomentumSum[0])
		# ys = self.angularMomentSums['ys']
		# ys.append(angularMomentumSum[1])
		# zes = self.angularMomentSums['zes']
		# zes.append(angularMomentumSum[2])
		self.angularMomentSums.append(norm(angularMomentumSum))
		return {'hanmiltonian' : self.hamiltionians, 'angularMomentum' : self.angularMomentSums}
		
	
		

