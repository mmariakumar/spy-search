from .agent import Agent

from ..model import model

class Planner(Agent):
    def __init__(self, model:model , query:str ):
        self.model = model
        self.output_model = [] 
    
    def run(self):
        """

        """
        pass 