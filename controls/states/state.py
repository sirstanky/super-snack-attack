from abc import ABC, abstractmethod


class State(ABC):

    @abstractmethod
    def run(self):
        pass
