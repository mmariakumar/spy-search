from .agent import Agent
from ..prompt.reporter import report_prompt , report_plan

from ..model import Model

class Reporter(Agent):
    def __init__(self, model:Model):
        self.model = model
        self.todo = []


    async def run(self , query , data=None):
        """
            based on query and data to write a response 
            Maybe we plan what to write and write a report style ? 
        """
        self._planner()


        prompt = report_prompt(query , data)
        r = self.model.completion(prompt)
        return {"agent":"TERMINATE" , "data": r , "task":""}

    def get_recv_format(self):
        pass 

    def get_send_format(self):
        pass

    def _planner(self , query):
        print("planning what to write")
        prompt = report_prompt(query)
        self.model.completion(prompt)


    def _task_handler(self):
        print("Handling taks")
    
    def _get_relevant_data(self):
        pass

