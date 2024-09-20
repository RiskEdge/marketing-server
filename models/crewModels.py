from pydantic import BaseModel
from typing import Optional

class AgentModel(BaseModel):
    role: str
    goal: str
    backstory: Optional[str] = None
    
class TaskModel(BaseModel):
    description:str
    agentName:str