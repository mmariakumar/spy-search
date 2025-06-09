from src import Planner
from src.factory import Factory
from src.model import Model

from src.main import generate_report
from src.utils import read_config

from src.api.app import router

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
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s",
)

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

