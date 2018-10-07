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


class Player(Simulator):
    def __init__(self, path: str):
        self.logfile = open(path, 'rb')
        self.history = pickle.load(self.logfile)
        self.n_step = 0

    def run_step(self):
        pos = (self.history[self.n_step]['pos'][:, 0], self.history[self.n_step]['pos'][:, 1], self.history[self.n_step]['pos'][:, 2])
        self.n_step = min(self.n_step+1, len(self.history)-1)
        print(self.n_step)
        return pos


class SimRun(Simulator):
    def __init__(self, n_steps: int = 10**10, n_stars: int = 10, universe: Universe = None, integrator: Integrator = Euler(), name: str = ""):
        assert isinstance(n_steps, int) and isinstance(integrator, Integrator) and isinstance(name, str)

        self.n_steps = n_steps
        self.epoch = 0
        self.integrator = integrator
        self.history = []

        if universe is None:
            self.universe = Universe(n_stars=n_stars)
        else:
            assert isinstance(universe, Universe)
            self.universe = universe

        if name == "":
            self.name = "{} {} {}".format(datetime.now(), self.n_steps, type(self.integrator).__name__.lower())
        else:
            self.name = name

        self.log_file_path = os.path.join(config.log_dir, 'test-'+self.name+'.bin')
        self.logfile = open(self.log_file_path, 'wb')
        self.simlog = ""

    def _save(self):
        self.logfile.write(self.simlog)
        self.simlog = ""
        self.logfile.flush()

    def run(self):
        # Initialize log file
        while self.run_step():
            pass
        pickle.dump(self.history, self.logfile)

    def run_step(self):
        self.simlog += "e:{},{}\n".format(self.epoch, str(self.universe))
        self.integrator.do_step(self.universe)
        # if self.epoch % 1000 == 0:
        #     self._save()
        self.history.append(np.copy(self.universe.stars))
        self.epoch += 1
        return self.epoch < self.n_steps

    def get_pos(self):
        return self.universe['pos'][:, 0], self.universe['pos'][:, 1], self.universe['pos'][:, 2]

    def __delete__(self, instance):
        self.logfile.flush()
        self.logfile.close()


if __name__ == '__main__':
    r = SimRun(n_steps=5)
    r.run()
