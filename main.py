from src.model.ollama import Ollama

o = Ollama(model="deepseek-r1:1.5b")
res = o.completion("test message" , stream=True)
print(res)