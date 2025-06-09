from fastapi import APIRouter ,UploadFile, File, Form
import json
import logging

logger = logging.getLogger(__name__)

from ..utils import read_config 
from .models.models import AgentsRequest , Message
from ..main import generate_report

from ..agent import Planner
from ..factory import Factory
from ..model import Model

from typing import List, Optional

router = APIRouter()


@router.get("/get_config")
async def get_config():
    config = read_config()
    return {"agents":config["agents"] , "provider":config["provider"] , "model":config["model"]}


@router.get("/select_folder")
async def select_folder():
    pass 

@router.post("/delete_folder")
async def delete_folder():
    pass 

@router.post("/create_folder")
async def create_folder():
    pass 

@router.get("/folder_list")
async def get_folder():
    pass

@router.post("/agents_selection")
async def select_agent(body: AgentsRequest):
    """
    Read the request
    ==> save it to the config.json
    shouldn't the config save in client side ?
    """
    arr = []
    for a in body.agents:
        arr.append(a)
    config = read_config()
    config["agents"] = arr
    config["provider"] = body.provider
    config["model"] = body.model 
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=4)
    return {"success": True, "agents_received": body.agents , "model_received":body.model , "provider_received":body.provider}



@router.post("/quick/{query}")
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
        "messages_received": [msg.model_dump() for msg in validated_messages],
    }


@router.post("/report/{query}")
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
            # TODO clean the local_files 
            content = await file.read()
            file_details.append({"filename": file.filename, "size": len(content)})

    logging.info("loading main ... ")
    r = await main(query, validated_messages)
    return {
        "report": r,
        "files_received": file_details,
        "messages_received": [msg.model_dump() for msg in validated_messages],
    }


"""
    TODO: refactor
"""
config = read_config()
quick_model: Model = Factory.get_model(config["provider"], config["model"])

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