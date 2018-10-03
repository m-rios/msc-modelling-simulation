import universe
import constants 
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
#envtrul

class Judger:
	"""docstring for Judger"""
	
	
	def __init__(self, judgedUniverse=None, judgedGalaxy=None):
		super(Judger, self).__init__()
		self.judgedUniverse=judgedUniverse
		self.judgedGalaxy = judgedGalaxy
		self.kineticEnergySums = []
		self.momentumSums = []
		self.potentialEnergySum = []

	def startJudging(self):
		if self.judgedUniverse != None:
			for galaxy in self.judgedUniverse:
				self.compareGalaxyByTimeSlot(slot=0.5, galaxy=galaxy)

		if self.judgedGalaxy:
			self.compareGalaxyByTimeSlot(slot=0.5, galaxy=self.judgedGalaxy)
			


	def metricsGalaxy(self, galaxy=None):
		galaxykineticEnergySum = 0
		galaxyMomentumSum = [0,0,0]
		galaxyPotentialEnergy = 0
		for star in galaxy:
			galaxykineticEnergySum += ((star.mass ** 2) * (star.vel[0]**2 + star.vel[1]**2+star.vel[2]**2)) / (2 * star.mass)
			galaxyMomentumSum += (star.mass * star.vel[0], star.mass * star.vel[1], star.mass * star.vel[2])

		for i in range(0, galaxy.n_stars):
			for  j in xrange(0, galaxy.n_stars):
				star1 = galaxy.stars[i]
				star2 = galaxy.stars[j]
				galaxyPotentialEnergy -= (constants.G * star1.mass * star2.mass)/(((star1.vel[0] - star2.vel[0]) ** 2 + (star1.vel[1] - star2.vel[1]) ** 2 + (star1.vel[2] - star2.vel[2]) ** 2) ** (1.0/2.0))

		self.kineticEnergySums.append(galaxyEnergySum)
		self.momentumSums.append(galaxyMomentumSum)
		self.galaxyPotentialEnergy.append(galaxyPotentialEnergy)

		plt.figure(figsize=(8, 6), dpi=80)
		plt.ion()
