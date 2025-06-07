from src import Planner
from src.agent.search import Search_agent
from src.agent.retrival import RAG_agent
from src.model.deepseek import Deepseek
from src.browser.crawl_ai import Crawl
from src.agent.reporter import Reporter

from src.router import Server, Router

from src.RAG.summary import Summary


STEP = 10


async def main(query):

    planner = Planner(model=Deepseek("deepseek-chat"), query=query)
    searcher = Search_agent(model=Deepseek("deepseek-chat"))
    rag = RAG_agent(model=Deepseek("deepseek-chat"))
    reporter = Reporter(model=Deepseek("deepseek-chat"))

    planner.add_model(
        model="searcher", description="Search latest information"
    )
    planner.add_model(
        model="reporter", description="generateing report"
    )

    server = Server()
    planner_router = Router(server, planner)
    searcher_router = Router(server , searcher)
    report_router = Router(server, reporter)

    server.add_router("planner", planner_router)
    server.add_router("searcher", searcher_router)
    server.add_router("reporter" , report_router)
    server.set_initial_router("planner", query)

    """
        all other agent set up  
    """
    print("Start running GO GO GO ...\n ")
    report = await server.start(query=query)
    report = report['data']
    #with open("report.md", "w", encoding="utf-8") as file:
     #   file.write(report + "\n\n") 
    #
    return report

    


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def test():
    return {"message" : "hello world"}


@app.get("/report/{query}")
async def report(query):
    r = await main(query)
    return {"report":r}
    
#    asyncio.run(main())
