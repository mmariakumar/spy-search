from langchain_community.tools import DuckDuckGoSearchRun , DuckDuckGoSearchResults


class DuckSearch:
    def __init__(self):
        self.search_engine = DuckDuckGoSearchResults(backend="text" , output_format="list")

    def search_result(self, query, k =5 , backend:str = "text"):
        result = self.search_engine.invoke(query)
        return result

#print(DuckSearch().search_result("test")[0]['snippet'])