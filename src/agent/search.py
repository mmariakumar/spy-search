from .agent import Agent
from ..model import model


class Search_agent(Agent):
    def __init__(self, model: model):
        self.model = model

    def run(self, task , data) -> str:
        """
            Search function need to user the brower methods to search relevant contents 
            - note that search agent should have it's own planner to plan search with what links
            - 
        """
        return {
            "agent":"TERMINATE"
        }

    def get_send_format(self):
        pass 

    def get_recv_format(self):
        pass