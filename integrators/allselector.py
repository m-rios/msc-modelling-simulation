from integrators.selector import Selector
from model.universe import Universe
import numpy as np


class AllSelector(Selector):

    def select(self, star_idx: int, universe: Universe) -> Universe:
        sub_universe = Universe()
        sub_universe.n_stars = universe.n_stars - 1
        sub_universe.stars = np.delete(universe.stars, star_idx)
        return sub_universe
