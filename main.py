from src import Planner
from src.model.deepseek import Deepseek
from src.browser.crawl_ai import Crawl
from src.RAG.summary import Summary

# TODO: read json ? 

STEP = 10

async def main():
    """
        workflow: 
            planner:
                state 1: no more planning / no more planning step / staisfy response ; action: return response
                state 2: more information about this subject is requried before writing report ; action: browser agent
                state 3: local information is needed (requrie by the use for example) ; action: send to local RAG query
                state 4: retrival information from previous round ; action: RAG query
                state 5: enough information to write the report / response ; action writer
            
            search:
                state 1: no more searching step ; action summarize current db --> send back to planner
                state 2: no next url in the searching space; action: based on available searching api --> search relevant information
                state 3: have next url --> search relevent content and script the list of available website (selected by LLM)
            
            retrival:
                state 1: no more searching step action terminate
                state 2: not enough content --> action: summary with local top k selected document [TODO: maybe save in sqlite3 ?] 
                state 3: enough content --> action return summary
    """
    p =Planner(model=Deepseek("deepseek-chat"))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())