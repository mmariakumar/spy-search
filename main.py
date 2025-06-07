from src import Planner
from src.agent.search import Search_agent
from src.model.deepseek import Deepseek
from src.agent.reporter import Reporter
from src.factory import Factory

from src.main import generate_report , read_config

from api.server import AgentsRequest
import json 

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

STEP = 10

async def main(query ,api:str = None):
    config = read_config()
    m = Factory.get_model(config['provider'] , config['model'])
    planner = Planner(m)
    agents = []
    for agent in config['agents']:
        agents.append(Factory.get_agent(agent , m))
    r  = await generate_report(query , planner , agents)
    return r

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/report/{query}")
async def report(query):
    r = await main(query)
    return {"report":r}


@app.post("/agents_selection")
async def select_agent(body: AgentsRequest):
    """
        Read the request 
        ==> save it to the config.json  
        shouldn't the config save in client side ? 
    """
    print("Parsed agents list:", body.agents)
    arr = [] 
    for a in body.agents:
        arr.append(a)
    config = read_config()
    config['agents'] = arr
    with open('./config.json' , 'w') as f:
        json.dump(config , f , indent=4)
    return {"success": True, "agents_received": body.agents}
