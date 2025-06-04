from src import Planner
from src.agent.search import Search_agent
from src.agent.retrival import RAG_agent
from src.model.deepseek import Deepseek
from src.browser.crawl_ai import Crawl

from src.router import Server, Router

from src.RAG.summary import Summary

# TODO: read json ?

STEP = 10


async def main():
    query = "Today's AI news "
    planner = Planner(model=Deepseek("deepseek-chat"), query=query)
    searcher = Search_agent(model=Deepseek("deepseek-chat"))
    rag = RAG_agent(model=Deepseek("deepseek-chat"))

    planner.add_model(
        model="searcher", description="Search latest information"
    )
    # planner.add_model(model="rag",description="Vector search relevant local content")
    # planner.add_model(model="reporter" , description="Summarize and write report based on given content")

    server = Server()
    planner_router = Router(server, planner)

    server.add_router("planner", planner_router)
    server.add_router("searcher", searcher)
    server.set_initial_router("planner", query)

    """
        all other agent set up  
    """

    server.start(query=query)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
