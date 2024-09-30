from pydantic import BaseModel
from typing import Optional

class AgentModel(BaseModel):
    role: str
    goal: str
    backstory: Optional[str] = None
    
class TaskModel(BaseModel):
    description:str
    agentName:str
    
class TopicRequest(BaseModel):
    topic:str
    
class ContextModel(BaseModel):
    company_name:str
    company_website:str
    industry:str
    agent: str
    services: Optional[str] = None
    competitors_context: Optional[str] = None
    content_type: str
    additional_info: Optional[str] = None