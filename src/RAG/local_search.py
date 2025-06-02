"""
This project use markitdown to handle local files. The key is to process types of document
to markdown
"""
from openai import OpenAI
from markitdown import MarkItDown

from .chrome import VectorSearch
from ..model import model

import hashlib

class LocalRAG():
    """
    Expected APIs:
        - convert any document to md
        - retrival based on query
        - convert to patch: set 1000 words per chunk ?
        - add new document to db
    """

    def __init__(self , model:model):
        """
            Args:
                db: Vector search 
        """
        self.vector_db = VectorSearch(name="local_search", path="./local_db")
        self.model = model

    def convert_to_markdown(self, path:str)->str:
        client = self.model.get_client()
        md= MarkItDown(llm_client = client , llm_model=self.model.get_model())
        result = md.convert(path)
        return result
    
    def add_document(self , path:str , k:int =1000):
        """
            Args:
                path: the path of that file
                k: how many word per patch , default set to be 1000 
            add_document will add the document to the db , ID with sha(256) content 
        """
        text = self.convert_to_markdown(path)
        words = text.split()
        patch = []
        counter = 0
        arr = [] 

        for word in words:
            counter += 1
            arr.append(word)
            if counter == (k-1):
                patch.append(arr.join(" "))
                arr = []
                counter = 0
    
        if counter != 0:
            patch.append(arr.join(" "))
        
        # now patch is an array of string 
        counter = 0 # reset counter for metadata
        for p in patch:
            self.vector_db.add_document(p , hashlib.sha256(p) , {"source":path , "patch":counter})
            counter += 1
        return 

    def search_document(self , query:str , k:int=1):
        return self.vector_db.query(query=query , k=k)

    def reset_db(self):
        self.vector_db.reset()