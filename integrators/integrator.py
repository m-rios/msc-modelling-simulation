from abc import ABC, abstractmethod


class Integrator(ABC):
    # Abstract integrator class. All integrator methods must extend this class

    @abstractmethod
    def do_step(self, universe):
        raise NotImplemented

