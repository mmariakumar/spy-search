from .model import Model
from ollama import chat 

class Ollama(Model):
    def __init__(self ,model:str):
        self.model = model
        self.message = [] 
    
    def completion(self, query:str , stream:str=False):
        res = chat(model=self.model , messages = [''])
         
        
    def _append_message(role:str , prompt:str):
        pass