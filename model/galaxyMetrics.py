import universe
import math
from datetime import datetime
from threading import Timer
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
#envtrul

class Judger:
	"""docstring for Judger"""
	self.lastEnergySum = 0
	self.lastMomentumSum = [0,0,0]
	self.energySums = []
	self.momentumSums = []
	self.t = None
	def __init__(self, judgedUniverse=None, judgedGalaxy=None):
		super(Judger, self).__init__()
		self.judgedUniverse=judgedUniverse
		self.judgedGalaxy = judgedGalaxy

	def startJudging(self):
		if self.judgedUniverse != None:
			for galaxy in self.judgedUniverse:
				self.compareGalaxyByTimeSlot(slot=0.5, galaxy=galaxy)

		if self.judgedGalaxy:
			self.compareGalaxyByTimeSlot(slot=0.5, galaxy=self.judgedGalaxy)
			


	def compareGalaxyByTimeSlot(self, slot=0.5, galaxy=None):
		galaxyEnergySum = 0
		galaxyMomentumSum = [0,0,0]
		for star in galaxy:
			galaxyEnergySum += star.mass * (star.vel[0]**2 + star.vel[1]**2+star.vel[2]**2)
			galaxyMomentumSum += (star.mass * star.vel[0], star.mass * star.vel[1], star.mass * star.vel[2])

		self.energySums.append(galaxyEnergySum)
		self.momentumSums.append(galaxyMomentumSum)

		if self.lastEnergySum != galaxyEnergySum:
			if self.lastEnergySum != 0:
				print ("error in metrics---kinect energy")
		if self.lastMomentumSum != galaxyMomentumSum:
			if self.lastMomentumSum[0] != 0 & self.lastMomentumSum[1] != 0 & self.lastMomentumSum[2] != 0:
				print ("error in metrics---momentum")

		self.lastEnergySum = galaxyEnergySum
		self.lastMomentumSum = galaxyMomentumSum
		plt.figure(figsize=(8, 6), dpi=80)
		plt.ion()

		self.t = Timer(slot, compareGalaxyByTimeSlot, (slot,galaxy,))
		self.t.start()

	def stopMetrics(self):
		self.t.cancel()

		

