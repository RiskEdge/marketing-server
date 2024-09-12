from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from crewai import Crew

from mycrew.agents import MarketingAgents
from mycrew.tasks import MarketingTasks

app = FastAPI()

load_dotenv()

origins = [
    "http://localhost:3000",
    "localhost:3000"
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
async def formInput(topic):
    agents = MarketingAgents()
    tasks = MarketingTasks()
    
    # AGENTS
    manager = agents.marketing_manager()
    # data_analyst = agents.data_analyst()
    competitor_analyst = agents.competitor_analyst()
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
            # data_analyst,
            competitor_analyst,
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
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {"result": result}
