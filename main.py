from src.model.gemini import Gemini

g = Gemini("gemini-2.5-flash")
print(g.completion("what is ai"))