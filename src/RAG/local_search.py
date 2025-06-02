"""
This project use markitdown to handle local files. The key is to process types of document
to markdown
"""
from openai import OpenAI
from markitdown import MarkItDown

from .chrome import VectorSearch
from ..model import model


class LocalRAG():
    """
    Expected APIs:
        - convert any document to md
        - retrival based on query
    """

    def __init__(self , db:VectorSearch , model:model):
        """
            Args:
                db: Vector search 
        """
        self.vector_db = db
        self.model = model

    def convert_to_markdown(self, path:str)->str:
        client = self.model.get_client()
        md= MarkItDown(llm_client = client , llm_model=self.model.get_model())
        result = md.convert(path)
        return result
    
if __name__ == "__main__":
    v = VectorSearch()
    from ..model.ollama import Ollama
    m = Ollama("deepseek-r1:1.5b") 
    l = LocalRAG(v , m)
    l.convert_to_markdown("./t.pdf")

