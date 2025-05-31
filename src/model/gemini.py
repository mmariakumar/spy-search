from google import genai #use openai seems better ?
import os 
from dotenv import load_dotenv

from .model import Model

class Gemini(Model):
    def __init__(self , model):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API")
        self.model = model
        self.client = genai.Client(api_key=self.api_key)

    def completion(self , query:str):
        # TODO: current generae content is not work
        res = self.client.models.generate_content(
            model="gemini-2.0-flash" , contents=query
        )
        return res 