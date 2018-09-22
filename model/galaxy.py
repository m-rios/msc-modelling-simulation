import numpy as np
from model.star import Star

class Galaxy:
    def __init__(self, n_stars=100):
        self.n_stars = n_stars
        self.stars = np.empty(n_stars, dtype=object)

        for idx in range(n_stars):
            self.stars[idx] = Star(pos=np.random.random(3), vel=np.random.random(3), acc=np.zeros(3), mass=float(np.random.random(1)))

