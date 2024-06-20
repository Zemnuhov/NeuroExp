from abc import ABC, abstractmethod


class Trigger(ABC):
    @abstractmethod
    def set_data(self, data):
        pass

    @abstractmethod
    def read_data(self):
        pass
