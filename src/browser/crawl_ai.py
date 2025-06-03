# we may use crew_ai write some api for it
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CacheMode , LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

from ..model import Model

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
    def __init__(self, model:Model , db=None , url_search = None):
        self.model = model
        self.crawler = AsyncWebCrawler()
        self.db = [] if db == None else db

        """
            The url_list is the list that we hope to search in the next ste 
            The url_search list is list of well known website that we want to search with 
        """
        self.url_list = []  
        self.url_search =[]

        self.broswer_conf = BrowserConfig(

        )
        self.run_conf = CrawlerRunConfig()

    async def start_crawler(self):
        await self.crawler.start()

    async def close_crawler(self):
        await self.crawler.close()

    # problem: still so slow --> for example searching takes 124.12s for arxiv website
    # TODO: concurrent process other state first ?
    async def get_url_llm(self , url , query):
        """
            Get url from a website with the help of llm
        """
        self.broswer_conf = BrowserConfig(
            headless=True
        )
        self.run_conf = CrawlerRunConfig(
            cache_mode = CacheMode.BYPASS,
            word_count_threshold=1,
            page_timeout=600,

            extraction_strategy=LLMExtractionStrategy(
                    llm_config=self.model.get_llm_config(),             
                    schema=_Url_result.model_json_schema(),
                    extraction_type="schema",
                    instruction=f"""
                    You are given the content of a search results webpage. Your task is to extract the main URL, the title of the webpage, and a brief description of the webpage. 
                    You should give ALL linked that are relevant to the content {query} 

                    - The URL should be the full link to the webpage.
                    - The title should be the main heading or the title of the webpage.
                    - The description should be a concise summary or snippet describing the webpage content.

                    Return the result strictly in the JSON schema format as defined:

                    {{
                    "url": "string",
                    "description": "string",
                    "title": "string"
                    }}

                    Only provide the JSON object without additional text or explanation.
                    """
            )
        )
        self.crawler = AsyncWebCrawler(
            config=self.broswer_conf
        )
        await self.start_crawler()

        result = await self.crawler.arun(
            url=url,
            config=self.run_conf
        )
        await self.close_crawler()
        # handle response instead of return result
        print(type(result))
        return result.extracted_content


    def screen_shot(self):
        pass 

    def search_content(self):
        pass 

    def run(self):
        pass 


class _Url_result(BaseModel):
    url: str = Field(... , description="the link")
    description: str = Field(... ,description="description of the website")
    title: str = Field(... , description="title of the webpage")


