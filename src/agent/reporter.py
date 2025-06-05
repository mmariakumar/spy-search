from .agent import Agent
from ..prompt.reporter import report_prompt

from ..model import Model

class Reporter(Agent):
    def __init__(self, model:Model):
        self.model = model


    async def run(self , response , data=None):
        """
            based on query and data to write a response 
        """
        prompt = report_prompt(response , data)
        r = self.model.completion(prompt)
        return {"agent":"TERMINATE" , "data": r , "task":""}

    def get_recv_format(self):
        pass 

    def get_send_format(self):
        pass

