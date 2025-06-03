from src import Planner
from src.model.deepseek import Deepseek
from src.browser.crawl_ai import Crawl

# TODO: read json ? 

async def main():
    """
        workflow: 
            planner:
                state 1: no more planning / no more planning step / staisfy response ; action: return response
                state 2: more information about this subject is requried before writing report ; action: browser agent
                state 3: local information is needed (requrie by the use for example) ; action: send to local RAG query
                state 4: retrival information from previous round ; action: RAG query
                state 5: enough information to write the report / response ; action writer
            
            browser:
                state 1: no more searching step ; action summarize current db --> send back to planner
                state 2: no next url in the searching space; action: based on available searching api --> search relevant information
                state 3: have next url --> search relevent content and script the list of available website (selected by LLM)
    """
    m = Deepseek("deepseek-chat")
    c = Crawl(m)
    result = await c.get_url_llm("https://arxiv.org/list/cs.CL/recent", "computer science papper")
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())