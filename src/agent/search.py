from .agent import Agent
from ..model import model


class Search_agent(Agent):
    def __init__(self, model: model):
        self.model = model

    def run(self, task , data) -> str:

        return {
            "agent":"TERMINATE"
        }

    def get_send_format(self):
        pass 

    def get_recv_format(self):
        pass