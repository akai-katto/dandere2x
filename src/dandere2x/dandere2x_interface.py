from abc import ABC, abstractmethod


# Abstract Class
class Dandere2xInterface(ABC):
    """
    Dandere2x now has two routes of operations (starting N different dandere2x instances, or one single instance)
    and functions needs to be abstracted outwards as a result. Unfortunately, starting dandere2x requires two different
    interfaces that will work with dandere2x differently in order to correctly handle both instances.
    """

    def __init__(self):
        pass

    @abstractmethod
    def pre_process(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def join(self):
        pass
