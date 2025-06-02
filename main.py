from src.RAG.chrome import VectorSearch
from src.RAG.local_search import LocalRAG


if __name__ == "__main__":
    v = VectorSearch()
    from src.model.ollama import Ollama
    m = Ollama("deepseek-r1:1.5b") 
    l = LocalRAG(m)
    l.add_document("./t.pdf")
    r = l.search_document("what is agent ?" , 3)
    print(r)

