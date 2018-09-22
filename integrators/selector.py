from abc import ABC, abstractmethod
from model.universe import Universe


class Selector(ABC):
    # Abstract selector class. Selector classes implement a way of choosing the stars that will be use to compute
    # gravitational pull to a particular star (i.e. optimizers)

    @abstractmethod
    def select(self, star_idx: int, universe: Universe) -> Universe:
        """

        :param star_idx: The index of the star for which select the attracting stars
        :param universe: Universe object that contains all the stars
        :return: A new universe which only contains the stars that will attract star_idx
        """
        raise NotImplemented
