from .agent import Agent
from ..prompt.reporter import report_prompt , report_plan

from ..model import Model

import string
import secrets
import json 

class Reporter(Agent):
    def __init__(self, model:Model):
        self.model:Model = model
        self.todo = []
        self.db = None
        self.source = {}

        self.length = 6  # the length of uuid 


    async def run(self , query:str , data=None):
        """
            based on query and data to write a response 
            Maybe we plan what to write and write a report style ? 
        """
        
        self.db = self.data_handler(data=data)
        short_summary = self.data_handler(data)

        res = self._planner(query=query)
        tasks = json.loads(self._extract_response(res))

        print(tasks)

        self._task_handler(tasks)

        prompt = report_prompt(query , short_summary)
        r = self.model.completion(prompt)



        return {"agent":"TERMINATE" , "data": r , "task":""}


    def data_handler(self, data):
        if not isinstance(data, list):
            print("error handling data")
            return

        short_summaries = []
        alphabet = string.ascii_letters + string.digits

        # Store processed items with IDs for future referencing
        processed_data = []

        for d in data:
            rand_id = ''.join(secrets.choice(alphabet) for _ in range(self.length))

            col = {
                'id': rand_id,
                'url': d.get('url', ""),
                'title': d.get('title', ""),
                'summary': d.get('summary', ""),
                'brief_summary': d.get('brief_summary', ""),
                'keywords': d.get('keywords', [])
            }
            processed_data.append(col)

            if col['summary'] != "":
                short_summaries.append({
                    "id": rand_id,
                    "short_summary": col['summary']
                })
        self.source = processed_data
        return short_summaries

    # Suppose you got a short summary id and want to get the long summary
    def get_source(self, summary_ids:list[int])->list[object]:
        sources =[]
        for item in self.processed_data:
            if item['id'] in summary_ids:
                sources.append(item)
        return sources

    def get_recv_format(self):
        pass 

    def get_send_format(self):
        pass

    def _planner(self , query):
        print("planning what to write")
        prompt = report_prompt(query , self.db)
        return self.model.completion(prompt)


    def _task_handler(self, tasks):
        print("handling tasks")
        for task in tasks:
            print(task)
    
    def _get_relevant_data(self):
        pass

