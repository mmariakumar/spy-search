from langchain_community.tools import DuckDuckGoSearchRun , DuckDuckGoSearchResults


class DuckSearch:
    def __init__(self):
        self.search_engine = DuckDuckGoSearchResults(backend="text" , output_format="list")
        self.news_engine = DuckDuckGoSearchResults(backend="news" , output_format="list" , num_results=9)

    def search_result(self, query, k =5 , backend:str = "text"):
        result = self.search_engine.invoke(query)
        return result
    
    def today_new(self , category:str):
        print(category)
        if category == "technology":
            category = "latest technology and sciences news"
        elif category == "finance":
            category = "latest finance news (market news)"
        elif category == "entertainment":
            category = "latest entertainment and culture"
        elif category == "sports":
            category = "latest sports news"
        elif category == "world":
            category = "latest world news"
        elif category == "health":
            category = "latest health and healthcare news"
        #print(category)
        res = self.news_engine.invoke(category + "news")
        return res
        #return []


#print(DuckSearch().search_result("test")[0]['snippet'])
#print(DuckSearch().today_new("tech"))