from pydantic import BaseModel
from typing import Optional, List

class AgentModel(BaseModel):
    role: str
    goal: str
    backstory: Optional[str] = None
    
class TaskModel(BaseModel):
    task_name: str
    description:str
    agentName:str
    
class ContextModel(BaseModel):
    company_name:str
    company_website:str
    industry:str
    # agent: str
    services: Optional[str] = None
    additional_info: Optional[str] = None
    llm: str = "ChatGPT"
    
class MarketingModel(ContextModel):
    competitors_context: Optional[str] = None
    
class ContentModel(ContextModel):
    topic:str
    content_type: str
    creativity: float = 0.5
    tags: Optional[str] = None #list[str] 
    
class InfoModel(BaseModel):
    company_name:str
    company_website:str
    industry:str
    # agent: str
    services: Optional[str] = None
    additional_info: Optional[str] = None
    llm: str = "ChatGPT"
    competitors_context: Optional[str] = None
    topic:str
    content_type: str
    creativity: float = 0.5
    tags: Optional[str] = None
    
    