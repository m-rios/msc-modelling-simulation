from abc import ABC, abstractmethod
from model import Universe
import numpy as np

class Selector(ABC):
    # Abstract selector class. Selector classes implement a way of choosing the stars that will be use to compute
    # gravitational pull to a particular star (i.e. optimizers)

    @abstractmethod
    def select(self, star_idx: int, universe: Universe) -> np.ndarray:
        """

        :param star_idx: The index of the star for which select the attracting stars
        :param universe: Universe object that contains all the stars
        :return: The indices of the stars that exert a force on star_idx
        """
        raise NotImplemented


class AllSelector(Selector):

    def select(self, star_idx: int, universe: Universe) -> np.ndarray:
        return np.concatenate((np.arange(star_idx), np.arange(star_idx+1, len(universe))))
