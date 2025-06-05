from .agent import Agent
from ..model import Model

from ..prompt.searcher import search_plan

class Search_agent(Agent):
    def __init__(self, model:Model, k: int = 10):
        """
        take some default URL for search
        k: number of steps
        """
        self.model = model

        self.search_web = [
            "https://google.com",
            "https://arxiv.com",
            "https://news.google.com",
            "https://scholar.google.com",
        ]

        self.todo = []
        self.step = 10

    def run(self, task, data) -> str:
        """
        Search function need to user the brower methods to search relevant contents
        - note that search agent should have it's own planner to plan search with what links

        Steps:
            1. Generate a to do list
            2. For each task
                read current short summary to plan the searching key word
                selecte the search_web
                allow one step depth search [hyper paramerter ?]
                script the content if irrelevant --> ignore
                if relevant --> self to db
                generate long short summary
            3. Return two things
                data: we want to reutrn the long summary
                for response we just need to response "FINISHED"
                AGENT: PLANNER
        """
        print("SEARCHER: RUNNING ")
        self._plan(task)
        return {"agent": "TERMINATE"}

    def get_send_format(self):
        pass

    def get_recv_format(self):
        pass

    def _plan(self , task:str):
        """
        Searcher planner
        """
        prompt = search_plan(task , self.todo)
        r = self.model.completion(prompt)
        print(r)

    def _task_handler(self , task:str):
        pass
