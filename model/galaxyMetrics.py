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
		self.hamiltionians = []
		self.angularMomentums = []
		

	def judge(self):
		# print('start!')
		angularMomentumSum = 0
		potentilEnergySum = 0
		kineticEnergySum = 0
		for i in range(len(self.judgedUniverse.stars)):
			currentStart = self.judgedUniverse.stars[i]
			pos = currentStart['pos']
			mass = currentStart['mass']
			vel = currentStart['vel']
			kineticEnergy = pow(norm(vel),2)/(2 * mass) 
			kineticEnergySum += kineticEnergy

			momentum = mass * vel
			angularMomentum = pos[0] * momentum[0] + pos[1] * momentum[1] + pos[2] * momentum[2]
			angularMomentumSum += angularMomentum

			for j in range(len(self.judgedUniverse.stars)):
				jStar = self.judgedUniverse.stars[j]
				jPos = jStar['pos']
				jMass = jStar['mass']

				if i != j:
					U = constants.G * mass * jMass / norm(pos - jPos)
					potentilEnergySum += U
		
		H = kineticEnergySum + potentilEnergySum
		
		self.hamiltionians.append(H)
		self.angularMomentums.append(angularMomentumSum)
		return {'hanmiltonian' : self.hamiltionians, 'angularMomentum' : self.angularMomentums}
		
	
		

