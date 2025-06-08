from src import Planner
from src.factory import Factory
from src.model import Model

from src.main import generate_report, read_config

from api.server import AgentsRequest
import json

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form

from pydantic import BaseModel
from typing import List, Optional

STEP = 10

import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s",
)


class Message(BaseModel):
    role: str
    content: str


config = read_config()
quick_model: Model = Factory.get_model(config["provider"], config["model"])


async def main(query, api: str = None):
    config = read_config()
    logging.info("finish reading config ...")

    m = Factory.get_model(config["provider"], config["model"])
    planner = Planner(m)
    logging.info("creating agents ... ")
    agents = []

    for agent in config["agents"]:
        m = Factory.get_model(config["provider"], config["model"])
        agents.append(Factory.get_agent(agent, m))

    logging.info(f"finish creating {agents}")
    logging.info("generating report ... ")

    r = await generate_report(query, planner, agents)

    logging.info("finish generating report")
    quick_model.messages.append({"role": "assistant", "content": r})
    return r


async def quick_response_logic(
    query: str,
    messages: List[Message],
    files: Optional[List[UploadFile]] = None,
    api: Optional[str] = None,
):
    # Example: call your model's completion method
    res = quick_model.completion(query)
    # You can also process messages or files here if needed
    return res


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


# TODO REFACTOR !
@app.post("/report/{query}")
async def report(
    query: str,
    messages: str = Form(...),  # JSON string of messages in form-data
    files: Optional[List[UploadFile]] = File(None),
):
    # Parse the messages JSON string to Python list
    logging.info("start generating report")
    try:
        messages_list = json.loads(messages)
    except json.JSONDecodeError:
        logging.error("invalid JSON in messages field")
        return {"error": "Invalid JSON in messages field"}

    # Validate each message dict using Pydantic (optional but recommended)
    validated_messages = [Message(**msg) for msg in messages_list]

    file_details = []
    if files:
        for file in files:
            content = await file.read()
            file_details.append({"filename": file.filename, "size": len(content)})

    logging.info("loading main ... ")
    r = await main(query, validated_messages)
    return {
        "report": r,
        "files_received": file_details,
        "messages_received": [msg.model_dump() for msg in validated_messages],
    }


@app.post("/quick/{query}")
async def quick_response_endpoint(
    query: str,
    messages: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    api: Optional[str] = Form(None),
):
    try:
        messages_list = json.loads(messages)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in messages field"}

    validated_messages = [Message(**msg) for msg in messages_list]

    res = await quick_response_logic(query, validated_messages, files, api)

    file_details = []
    if files:
        for file in files:
            content = await file.read()
            file_details.append({"filename": file.filename, "size": len(content)})

    return {
        "report": res,
        "files_received": file_details,
        "messages_received": [msg.dict() for msg in validated_messages],
    }


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
    config["agents"] = arr
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=4)
    return {"success": True, "agents_received": body.agents}


@app.post("/model_selection")
async def model_selection():

    return {"Error": "Not yet support"}
