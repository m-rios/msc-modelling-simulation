import math
import sys
sys.path.append('/Users/zhangyuanqing/Documents/Groningen/simulationAndModelling/msc-modelling-simulation/model') 
import universe

def leapfrogCalculating(calculatedUniverse, timeStep):

    for star in calculatedUniverse.n_stars:
        starhalfstep = star.pos + (timeStep * star.vel) / 2 # 13a
        star.pos = starhalfstep
    for star in calculatedUniverse.n_stars:
        star.acc = calculatedUniverse.getAccelerationOnStar(star) # new acceleration
        
    for star in calculatedUniverse.n_stars:
        star.vel = star.vel + timeStep * star.acc #get new vel (13b)
        star.pos = star.pos + timeStep * star.vel / 2
