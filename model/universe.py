import numpy as np
from model.galaxy import Galaxy


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

    # def get_velocities(self):
    #     velocities = np.empty((3, self.n_stars))
    #     for idx in range(self.n_stars):
    #         velocities[idx] = self.stars[idx].vel
    #
    # def get_positions(self):
    #     positions = np.empty((3, self.n_stars))
    #     for idx in range(self.n_stars):
    #         positions[idx] = self.stars[idx].pos
    #
    # def get_accelerations(self):
    #     accelerations = np.empty((3, self.n_stars))
    #     for idx in range(self.n_stars):
    #         accelerations[idx] = self.stars[idx].acc

