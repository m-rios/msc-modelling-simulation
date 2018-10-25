import numpy as np
from galpy.df import dehnendf
import math

import random

import sys



class Universe:
    def __init__(self, n_stars=100, star_array=None, mass=1e5):
        self.mass = mass
        self.__star_fields = [('pos', (np.float64, 3)),
                                              ('vel', (np.float64, 3)),
                                              ('acc', (np.float64, 3)),
                                              ('acc2', (np.float64, 3)),
                                              ('acc3', (np.float64, 3)),
                                              ('mass', np.float64)]

        if star_array is not None:
            self.stars = star_array
        else:
            self.stars = np.empty(0, self.__star_fields)
            # self.stars = np.zeros(n_stars, dtype=self.__star_fields)
            # self.stars['pos'] = np.random.randn(n_stars, 3)
            # self.stars['pos'][:, 2] = 0
            # self.stars['vel'] = np.random.randn(n_stars, 3)
            # self.stars['vel'][:, 2] = 0
            # self.stars['acc'] = np.zeros((n_stars, 3))
            # self.stars['mass'] = np.random.rand(n_stars)

            # self.add_galaxy(1e10, 3, 2, n_stars)
            self.add_galaxy(self.mass, n_stars, [1, 0, 0], 0, [0, 0, 0])
            # self.add_galaxy(self.mass, n_stars, [1, 0, 0], 0, [0, -3, 0])

    def add_galaxy(self, mass, n_stars, axis, theta, tras):
        tras = np.asarray(tras)
        R = Universe.rotation_matrix(axis, theta)
        dfc = dehnendf(beta=0.)
        o = dfc.sample(n=n_stars, returnOrbit=True)
        stars = np.zeros(n_stars, dtype=self.__star_fields)
        mass = random.randint(1e2, 1e10)
        for idx in range(len(stars)):
            stars['pos'][idx, 0:2] = [o[idx].x(), o[idx].y()]
            stars['mass'][idx] = mass
            # Get velocity from angular velocity of sample
            tangential = np.linalg.norm(stars['pos'][idx, 0:2])*o[idx].vT()
            unit_pos = stars['pos'][idx, 0:2]/np.linalg.norm(stars['pos'][idx, 0:2])
            unit_vel = np.array([-unit_pos[1], unit_pos[0]])  # 90 deg rotated counterclockwise
            stars['vel'][idx, 0:2] = unit_vel * tangential
            stars['pos'][idx] = np.dot(R, stars['pos'][idx]) + tras
        self.stars = np.append(self.stars, stars)

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

    @staticmethod
    def rotation_matrix(axis, theta):
        """
        From version of https://stackoverflow.com/questions/6802577/rotation-of-3d-vector
        """
        axis = np.asarray(axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


if __name__ == '__main__':
    args = sys.argv
    assert len(args) == 3, "Usage: universe n_stars mass"
    # Export universe to csv
    u = Universe(n_stars=int(args[1]), mass=float(args[2]))
    stars = []
    for star in u:
        fields = [str(p) for p in star['pos']] + [str(v) for v in star['vel']] + [str(star['mass'])]
        stars.append(','.join(fields))
    content = '\n'.join(stars)
    with open('universe.csv', 'w') as f:
        f.write(content)
