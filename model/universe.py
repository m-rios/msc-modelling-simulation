import numpy as np
from scipy import stats
from galpy.df import dehnendf

class Galaxy:

    def __init__(self, m, a, b):
        self.m = m
        self.a = a
        self.b = b
        self.norm = stats.norm()
        print(self.norm.rvs())

    def _density(self, R, z):
        t1 = (self.b**2 * self.m)/4*np.pi
        t2 = self.a*R**2 +(self.a + 3*(z**2 + self.b**2)**(1/2))*(self.a+(z**2 + self.b**2)**(1/2))**2
        t3 = (R**2 + (self.a + (z**2 + self.b**2)**1/2)**2)**(2/5)*(z**2+self.b**2)**(3/2)
        return t1 * (t2/t3)

    def sample_galaxy(self):
        pass


class Universe:
    def __init__(self, n_stars=100, star_array=None):
        self.__star_fields = [('pos', (np.float64, 3)),
                                              ('vel', (np.float64, 3)),
                                              ('acc', (np.float64, 3)),
                                              ('acc2', (np.float64, 3)),
                                              ('acc3', (np.float64, 3)),
                                              ('mass', np.float64)]

        if star_array is not None:
            self.stars = star_array
        else:
            self.stars = np.zeros(n_stars, dtype=self.__star_fields)
            self.stars['pos'] = np.random.randn(n_stars, 3)
            self.stars['pos'][:, 2] = 0
            self.stars['vel'] = np.random.randn(n_stars, 3)
            self.stars['vel'][:, 2] = 0
            self.stars['acc'] = np.zeros((n_stars, 3))
            self.stars['mass'] = np.random.rand(n_stars)*1e10

            # self.add_galaxy(1e10, 3, 2, n_stars)
            self.add_galaxy(1, n_stars)

    def add_galaxy(self, mass, n_stars):
        dfc = dehnendf(beta=0.)
        o = dfc.sample(n=n_stars, returnOrbit=True)
        self.stars = np.zeros(n_stars, dtype=self.__star_fields)
        for idx in range(len(self.stars)):
            self.stars['pos'][idx, 0:2] = [o[idx].x(), o[idx].y()]
            self.stars['mass'][idx] = mass
            # Get velocity from angular velocity of sample
            tangential = np.linalg.norm(self.stars['pos'][idx, 0:2])*o[idx].vT()
            unit_pos = self.stars['pos'][idx, 0:2]/np.linalg.norm(self.stars['pos'][idx, 0:2])
            unit_vel = np.array([-unit_pos[1], unit_pos[0]])  # 90 deg rotated counterclockwise
            self.stars['vel'][idx, 0:2] = unit_vel * tangential


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
        assert isinstance(other, Universe)
        u3 = Universe(n_stars=0)
        u3.stars = np.concatenate((self.stars, other.stars))
        return u3

    def __getitem__(self, item):
        return self.stars[item]

    def __setitem__(self, key, value):
        self.stars[key] = value

    def __delitem__(self, idx):
        self.stars = np.delete(self.stars, idx)


if __name__ == '__main__':
    print(Galaxy(1,1,1))
