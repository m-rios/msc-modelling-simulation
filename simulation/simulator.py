from simulation.integrator import Integrator, Euler
from abc import ABC, abstractmethod
from model import Universe
from datetime import datetime
import config
import os
import pickle
import numpy as np


class Simulator(ABC):
    @abstractmethod
    def run_step(self):
        raise NotImplemented

    def get_uni(self) -> Universe:
        raise NotImplemented

    def get_pos(self) -> (np.ndarray, np.ndarray, np.ndarray):
        raise NotImplemented


class Player(Simulator):
    def __init__(self, path: str):
        self.logfile = open(path, 'rb')
        self.universe = pickle.load(self.logfile)
        self.n_step = 0

    def run_step(self):
        try:
            self.universe = pickle.load(self.logfile)
        except EOFError:
            pass

    def get_uni(self):
        return self.universe

    def get_pos(self):
        return self.universe['pos'][:, 0], self.universe['pos'][:, 1], self.universe['pos'][:, 2]


class SimRun(Simulator):
    def __init__(self, n_steps: int = 10**10, n_stars: int = 10, universe: Universe = None, integrator: Integrator = Euler(), name: str = ""):
        assert isinstance(n_steps, int) and isinstance(integrator, Integrator) and isinstance(name, str)

        self.n_steps = n_steps
        self.epoch = 0
        self.integrator = integrator

        if universe is None:
            self.universe = Universe(n_stars=n_stars)
        else:
            assert isinstance(universe, Universe)
            self.universe = universe

        if name == "":
            self.name = "test_{}_steps_{}_stars_{}_{}".format(datetime.now(), self.n_steps, len(self.universe), type(self.integrator).__name__.lower())
        else:
            self.name = name

        self.log_file_path = os.path.join(config.log_dir, self.name+'.bin')
        self.logfile = open(self.log_file_path, 'wb')
        self.history = []

    def _save(self):
        print("saving "+str(self.epoch))
        pickle.dump(self.universe, self.logfile)

    def run(self):
        # Initialize log file
        while self.run_step():
            pass

    def run_step(self):
        self.integrator.do_step(self.universe)
        self._save()
        self.epoch += 1
        return self.epoch < self.n_steps

    def get_pos(self):
        return self.universe['pos'][:, 0], self.universe['pos'][:, 1], self.universe['pos'][:, 2]

    def get_uni(self):
        return self.universe

    def __del__(self):
        self.logfile.flush()
        self.logfile.close()
        print('SimRun died')


if __name__ == '__main__':
    r = SimRun(n_steps=5)
    r.run()
