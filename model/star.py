import numpy as np
import random as rnd


class Star:
    def __init__(self, pos=np.random.random(3), vel=np.random.random(3), acc=np.zeros(3), mass=rnd.random()):
        # WARNING: the above initialization seems to yield the same value every time
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.mass = mass

    def __str__(self):
        return str(list(self.pos)+list(self.vel)+list(self.acc)+list([self.mass]))
