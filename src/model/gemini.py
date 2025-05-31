from google import genai 
from google.genai import types 

import os 
from dotenv import load_dotenv

from .model import Model

class Gemini(Model):
    def __init__(self , model):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API")
        self.model = model
        self.client = genai.Client(api_key=self.api_key)
        self.message = self.client.chats.create(model=model)

    def completion(self , query:str):
        res = self.message.send_message(query)
        return res.text

    def reset(self):
        """
            Reset chat message
        """
        self.message = self.client.chats.create(model=Model)

    def add_system_instruction(self, instruction:str):
        self.message.send_message(config=types.GenerateContentConfig(
            system_instruction=instruction)
        )
