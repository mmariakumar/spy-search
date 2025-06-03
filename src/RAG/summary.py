"""
    This file provide method so summaries content with long length with LLM
"""
from ..model import Model
from ..prompt import summary_prompt

from pydantic import BaseModel, Field
import json
import re

class Summary(object):
    def __init__(self ,model:Model , k:int = 10000):
        self.model = model
        self.db = []
        self.result = [] 
        # k corresponding to the chunk  
        self.k = k 
        self.chunks:list[str] = [] 
    
    def summary(self , content:str):
        texts = content.split()
        counter = 0 
        paragraph = ""
        
        for text in texts:
            counter += 1 
            paragraph += (text + " ")
            if counter >= self.k:
                self.chunks.append(paragraph)
                paragraph = ""
                counter = 0
        self.chunks.append(paragraph)
        for chunk in self.chunks:
            prompt = summary_prompt(chunk, self.db)
            r = self.model.completion(prompt)  # r is the raw LLM response string
            json_str = self.extract_json_from_codeblock(r)
            if json_str is None:
                print("No JSON code block found in response")
                continue

            try:
                response_dict = json.loads(json_str)
                response_obj = _Response(**response_dict)
                
                full_summary = response_obj.full_summary
                short_summary = response_obj.short_summary

                self.db.append(short_summary)
                self.result.append(full_summary)

            except:
                print(f"Failed to parse or validate JSON summary")

        return '\n'.join(self.result) 
                
    
    def extract_json_from_codeblock(self, text: str) -> str | None:
        pattern = r"```json\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)
        return None

            
         

class _Response(BaseModel):
    full_summary: str 
    short_summary:str 

