# we may use crew_ai write some api for it
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CacheMode
class Crawl:
    """
    Crawl4ai should be used to support browser.py [Maybe we don't even need browser.py]
    with browser.py search some well known website for example google arxiv google scholar
    or some user self defined website --> seach all link

    --> then use crawl4ai to help for search

    All api is expected to be sync and use crawl4ai
    Expected API list
        get_links: given a url which is the result from a search website like google return the result list of that page
        get_images: get all images from the webpage
        get_content: get relevant content to a markdown
    """
    def __init__(self, model , db=None , url_search = None):
        self.model = model
        self.crawler = AsyncWebCrawler()
        self.db = [] if db == None else db

        """
            The url_list is the list that we hope to search in the next ste 
            The url_search list is list of well known website that we want to search with 
        """
        self.url_list = []  
        self.url_search =[]

        self.broswer_conf = BrowserConfig()
        self.run_conf = CrawlerRunConfig()

    async def start_crawler(self):
        await self.crawler.start()

    async def close_crawler(self):
        await self.crawler.close()


    async def get_url_llm(self):
        """
            Get url from a website with the help of llm
        """
        pass 


    def screen_shot(self):
        pass 

    def search_content(self):
        pass 

    def run(self):
        pass 


if __name__ == "__main__":
    pass
