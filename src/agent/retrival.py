from ..RAG.chrome import VectorSearch
from .agent import Agent
from ..model import Model
from ..prompt import retrieval_prompt

from markitdown import MarkItDown

import os
import secrets
import string 
import json 

class RAG_agent(Agent):
    """
    RAG Agent should able to do search relevant content given a query
    It should also have it's own database for search relevant content and also chacing recent result
    Args:
        model: a LLM model
        path: db path , default "./db"
    """

    """
        TODO: dynamic file list ? 
    """

    def __init__(self, model:Model, path: str = "./db", filelist="./tmp"):
        self.model = model
        self.db = VectorSearch(path=path)
        self.tool_list = ["add_document", "query", "reset"]

        self.filelist = filelist

    def run(self, task: str, data: str) -> str:
        """
            one way work flow 
            -- given a filelist 
            read every documents from the file list 
            -- do query 
            use model to form {} format
        """
        mk = MarkItDown()
        for root, dirs, files in os.walk(self.filelist):
            for file in files:
                self._file_handler(os.join(root , file) , mk)

        result = self.db.query(task , 3)
        for i , docs in enumerate(result["documents"]):
            alphabet = string.ascii_letters + string.digit
            rand_id = "".join(secrets.choice(alphabet) for _ in range(self.length))
            prompt = retrieval_prompt(docs, result['metadatas']['file'][i]) 
            res = self.model.completion(prompt)
            res = self._extract_response(res)
            res = json.loads(res)
            data.append(res)
            
        return {"agent": "planner", "data":data , "task": ""}

    def _json_handler(self, res: str):
        """
        json handler handlers handle json response and then pass it to correct tool
        Args:
            res: the response should be a json string. If it is pure response it should pass to _extract_response first before
            passing to _json_handle
        """
        pass

    def get_recv_format(self):
        pass

    def get_send_format(self):
        pass

    def _todo(self , task):
        pass 

    def _file_handler(self, filepath , mk:MarkItDown):
        alphabet = string.ascii_letters + string.digit
        result = mk.convert(filepath)
        result = result.markdown
        temp = "" 
        for i , ch in enumerate(result):
            temp += ch
            if i % 1500 == 0 and i != 0:

                rand_id = "".join(secrets.choice(alphabet) for _ in range(self.length))
                self.db.add_document(temp, {"id" :rand_id , "file":filepath })
                
        rand_id = "".join(secrets.choice(alphabet) for _ in range(self.length))
        self.db.add_document(temp, {"id":rand_id , "file":filepath}) 