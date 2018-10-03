import numpy as np


class Universe:
    def __init__(self, n_stars=100):
        self.stars = np.zeros(n_stars, dtype=[('pos', (np.float64, 3)),
                                              ('vel', (np.float64, 3)),
                                              ('acc', (np.float64, 3)),
                                              ('acc2', (np.float64, 3)),
                                              ('acc3', (np.float64, 3)),
                                              ('mass', np.float64)])
        for star in self.stars:
            star['pos'] = np.random.randn(3)
            star['vel'] = np.random.randn(3)
            star['acc'] = np.random.rand(3)
            star['mass'] = np.random.rand()*10000

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

    def __delitem__(self, idx):
        self.stars = np.delete(self.stars, idx)
