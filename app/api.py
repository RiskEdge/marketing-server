from dotenv import load_dotenv

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from crewai import Crew

from mycrew.agents import MarketingAgents
from mycrew.tasks import MarketingTasks

from models.crewModels import AgentModel, TaskModel

from pydantic import BaseModel

class TopicRequest(BaseModel):
    topic:str

app = FastAPI()

load_dotenv()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
async def index() -> dict:
    return {"message" : 'Hello World'}

@app.post('/form-input')
async def formInput(topic:TopicRequest):
    
    topic = topic.topic
    
    agents = MarketingAgents()
    tasks = MarketingTasks()

    # AGENTS
    manager = agents.marketing_manager()
    competitor_analyst = agents.competitor_analyst()
    # competitor_analyst = agents.competitor_analyst()
    content_creator = agents.content_creator()
    SEO_specialist = agents.SEO_specialist()

    # TASKS
    manager_task = tasks.marketing_management(manager, topic)
    # data_analyst_task = tasks.data_analysis(data_analyst, topic)
    competitor_analyst_task = tasks.competitor_analysis(competitor_analyst, topic)
    content_creator_task = tasks.content_creation(content_creator, topic)
    SEO_specialist_task = tasks.SEO(SEO_specialist, topic)
    crew = Crew(
        agents = [
            manager,
            competitor_analyst,
            # competitor_analyst,
            content_creator,
            SEO_specialist
        ],
        tasks = [
            manager_task,
            # data_analyst_task,
            competitor_analyst_task,
            content_creator_task,
            SEO_specialist_task
        ],
        verbose=True,
        full_output=True,
        planning=True,
        output_log_file='outputs/output6.md'
    )
    
    result = crew.kickoff()
    
    manager_task_output = manager_task.output
    competitor_analyst_task_output = competitor_analyst_task.output
    content_creator_task_output = content_creator_task.output
    SEO_specialist_task_output = SEO_specialist_task.output
    
    return {"result": result} 

@app.get('/agents-info')
def sendAgentInfo():
    agents = MarketingAgents()
    tasks = MarketingTasks()

    # AGENTS
    manager = agents.marketing_manager()
    # data_analyst = agents.data_analyst()
    competitor_analyst = agents.competitor_analyst()
    content_creator = agents.content_creator()
    SEO_specialist = agents.SEO_specialist()

    # TASKS
    manager_task = tasks.marketing_management(manager)
    # data_analyst_task = tasks.data_analysis(data_analyst, topic)
    competitor_analyst_task = tasks.competitor_analysis(competitor_analyst)
    content_creator_task = tasks.content_creation(content_creator)
    SEO_specialist_task = tasks.SEO(SEO_specialist)
    return {
       "agents": {
        "manager": AgentModel(role=manager.role, goal=manager.goal, backstory=manager.backstory),
        "competitor_analyst": AgentModel(role=competitor_analyst.role, goal=competitor_analyst.goal, backstory=competitor_analyst.backstory),
        "content_creator": AgentModel(role=content_creator.role, goal=content_creator.goal, backstory=content_creator.backstory),
        "SEO_specialist": AgentModel(role=SEO_specialist.role, goal=SEO_specialist.goal, backstory=SEO_specialist.backstory),
        },
       "tasks":{
           "manager_task": TaskModel(description=manager_task.description, agentName=manager_task.agent.role),
           "competitor_analyst_task": TaskModel(description=competitor_analyst_task.description, agentName=competitor_analyst_task.agent.role),
           "content_creator_task": TaskModel(description=content_creator_task.description, agentName=content_creator_task.agent.role),
           "SEO_specialist_task": TaskModel(description=SEO_specialist_task.description, agentName=SEO_specialist_task.agent.role),
        }
    }
    