from ..RAG.chrome import VectorSearch
from .agent import Agent
from ..prompt import retrival_agent_prompt

import json
import re


class RAG_agent(Agent):
    """
    RAG Agent should able to do search relevant content given a query
    It should also have it's own database for search relevant content and also chacing recent result
    Args:
        model: a LLM model
        path: db path , default "./db"
    """

    def __init__(self, model, path: str = "./db" , name = "local_db"):
        self.model = model
        self.db = VectorSearch(path=path , name=name)
        self.tool_list = ["add_document", "query", "reset"]

    async def run(self, task: str , data) -> str:
        # when rest ? 
        """
        workflow:
             
        """
        print("handling retrival")

        # data should always use the same format as retrival ? 

        # data should always append

        # dk too

        return {"agent":"planner" , "data":data , "task" : ""}
  

    def _json_handler(self, res: str):
        """
        json handler handlers handle json response and then pass it to correct tool
        Args:
            res: the response should be a json string. If it is pure response it should pass to _extract_response first before
            passing to _json_handle
        """
        obj = json.loads(res)
        print(obj)
        print(obj["tool"])
        print(obj["args"])

    def get_recv_format(self):
        pass

    def get_send_format(self):
        pass
