from src.agent.retrival_agent import RAG_agent
from src.model.ollama import Ollama

m = Ollama("deepseek-r1:1.5b")

a = RAG_agent(m)

print(a.run("Search prompble relaterd to tesla "))
