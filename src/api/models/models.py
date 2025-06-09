from typing import List
from pydantic import BaseModel


class AgentsRequest(BaseModel):
    agents: List[str]  # List of strings
    model: str
    provider:str

class FolderRequest(BaseModel):
    db :str


class Message(BaseModel):
    role: str
    content: str