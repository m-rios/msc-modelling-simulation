import math
import sys
sys.path.append('/Users/zhangyuanqing/Documents/Groningen/simulationAndModelling/msc-modelling-simulation/model') 
import universe

def leapfrogCalculating(star, timeStep):
    
    halfLocation = star.pos + timeStep * star.pos / 2
    veloN2 = star.vel  + timeStep * star.acc * halfLocation
    locationN2 = halfLocation + timeStep * veloN2 / 2

    star.vel = veloN2
    star.pos = locationN2
