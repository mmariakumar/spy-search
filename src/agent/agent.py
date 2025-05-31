from abc import ABC, abstractmethod

"""
    This is an abstract class for Agent
    Here we will list out method that an Agent should have 
"""
class Agent(ABC):

    @abstractmethod
    def __init__(self, model):
        pass 
    """
        An agent should have a run method such that it can run it's workflow 
        NOTE: choosing right tool for the right job should also place in the run method
    """
    @abstractmethod
    def run(self):
        pass 