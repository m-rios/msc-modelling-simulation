import numpy as np


class Star:
    def __init__(self, pos=np.random.random(3), vel=np.random.random(3), acc=np.zeros(3), mass=float(np.random.random(1))):
        # WARNING: the above initialization seems to yield the same value every time
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.mass = mass

    def __str__(self):
        superlist = list(self.pos)+list(self.vel)+list(self.acc)+list([self.mass])
        return ','.join(map(str, superlist))


class Galaxy:
    def __init__(self, n_stars=100, name="galaxy1"):
        self.n_stars = n_stars
        self.stars = np.empty(n_stars, dtype=object)
        self.name = name

        for idx in range(n_stars):
            self.stars[idx] = Star(pos=np.random.random(3), vel=np.random.random(3), acc=np.zeros(3), mass=float(np.random.random(1)*100))

    def __len__(self):
        return len(self.stars)

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.stars):
            star = self.stars[self.idx]
            self.idx += 1
            return star
        else:
            raise StopIteration

    def __str__(self):
        return ';'.join(str(s) for s in self)

    def __add__(self, other):
        assert isinstance(other, Galaxy)
        g3 = Galaxy(n_stars=0)
        g3.stars = np.concatenate((self.stars, other.stars))
        g3.__n_stars = len(g3.stars)
        return g3

    def __getitem__(self, item):
        return self.stars[item]

    def __delitem__(self, idx):
        self.stars = np.delete(self.stars, idx)


class Universe:
    def __init__(self, n_stars: int= 100, galaxy1: Galaxy = None, galaxy2: Galaxy = None):
        """
        Initializes the universe either with a random distribution of n_stars or as a merge of two galaxies.
        The goal fo the Universe class is to contain all the stars to be simulated by the integrators.
        :param n_stars: The number of stars that will be randomly initialize
        :param galaxy1: Object of type Galaxy
        :param galaxy2: Object of type Galaxy
        """

        if galaxy1 is not None and galaxy2 is not None:
            assert isinstance(galaxy1, Galaxy) and isinstance(galaxy2, Galaxy)
            self.galaxy = galaxy1 + galaxy2
        else:
            self.stars = Galaxy(n_stars).stars
            self.galaxy = Galaxy(n_stars)

if __name__ == '__main__':
    g = Galaxy()
    a = g[1]
    del g[1]
