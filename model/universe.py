import numpy as np


class Star:
    def __init__(self, pos=np.random.random(3), vel=np.random.random(3), acc=np.zeros(3), mass=float(np.random.random(1))):
        # WARNING: the above initialization seems to yield the same value every time
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.mass = mass

    def __str__(self):
        return str(list(self.pos)+list(self.vel)+list(self.acc)+list([self.mass]))


class Galaxy:
    def __init__(self, n_stars=100, name="galaxy1"):
        self.n_stars = n_stars
        self.stars = np.empty(n_stars, dtype=object)
        self.name = name

        for idx in range(n_stars):
            self.stars[idx] = Star(pos=np.random.random(3), vel=np.random.random(3), acc=np.zeros(3), mass=float(np.random.random(1)))


class Universe:
    def __init__(self, n_stars: int= 100, galaxy1: Galaxy = None, galaxy2: Galaxy = None):
        """
        Initializes the universe either with a random distribution of n_stars or as a merge of two galaxies.
        The goal fo the Universe class is to contain all the stars to be simulated by the integrators.
        :param n_stars: The number of stars that will be randomly initialize
        :param galaxy1: Object of type Galaxy
        :param galaxy2: Object of type Galaxy
        """

        self.n_stars = n_stars
        self.stars = None # List of star objects
        if galaxy1 is not None and galaxy2 is not None:
            assert isinstance(galaxy1, Galaxy) and isinstance(galaxy2, Galaxy)
            self.stars = np.concatenate((galaxy1.stars, galaxy2.stars))
            self.n_stars = len(self.stars)
        else:
            self.stars = Galaxy(n_stars).stars

