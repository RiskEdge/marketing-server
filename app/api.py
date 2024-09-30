from dotenv import load_dotenv

from fastapi import FastAPI, Body, Query
from fastapi.middleware.cors import CORSMiddleware

from crewai import Crew
from crewai.process import Process

from mycrew.agents import MarketingAgents
from mycrew.tasks import MarketingTasks

from models.crewModels import AgentModel, TaskModel, ContextModel, TopicRequest

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
async def formInput(context: ContextModel = Body(...)):
    try:
        agents = MarketingAgents()
        tasks = MarketingTasks()
        print(context)
            
        # MANAGER
        manager = agents.marketing_manager()

        # MANAGER TASK
        manager_task = tasks.marketing_management(manager, context)

        if context.agent == "marketing_analyst":
            marketing_analyst = agents.marketing_analyst()
            marketing_analyst_task = tasks.marketing_analysis(marketing_analyst, context)
            
            marketing_analysis_crew = Crew(
            agents = [
                marketing_analyst,
                
            ],
            tasks = [
                marketing_analyst_task,
                
            ],
            manager_agent=manager,
            verbose=True,
            full_output=True,
            planning=True,
            output_log_file='outputs/marketingOutput/output3.md'
            )
            
            result = marketing_analysis_crew.kickoff()
            return {"result": result} 
        
        elif context.agent == "SEO_specialist":
            SEO_specialist = agents.SEO_specialist()
            SEO_specialist_task = tasks.SEO(SEO_specialist, context)
            
            seo_crew = Crew(
            agents = [
                SEO_specialist,
            ],
            tasks = [
                SEO_specialist_task,
            ],
            manager_agent=manager,
            verbose=True,
            full_output=True,
            planning=True,
            output_log_file='outputs/seo/output3.md'
            )
        
            result = seo_crew.kickoff()
            return {"result": result} 
        
        elif context.agent == "content_creator":
            content_creator = agents.content_creator()
            content_creator_task = tasks.content_creation(content_creator, context)
            
            content_creation_crew = Crew(
            agents = [
                content_creator,
            ],
            tasks = [
                content_creator_task,
            ],
            manager_agent=manager,
            verbose=True,
            full_output=True,
            planning=True,
            output_log_file='outputs/contentCreation/output3.md'
            )
            
            result = content_creation_crew.kickoff()
            return {"result": result} 
        
        
        
    except Exception as e:
        print(e)

@app.post('/agents-info')
def sendAgentInfo(context: ContextModel = Body(...)):
    try:
        agents = MarketingAgents()
        tasks = MarketingTasks()
        
        # AGENTS
        manager = agents.marketing_manager()
        marketing_analyst = agents.marketing_analyst()
        content_creator = agents.content_creator()
        SEO_specialist = agents.SEO_specialist()
        
        # TASKS
        manager_task = tasks.marketing_management(manager, context=context)
        marketing_analyst_task = tasks.marketing_analysis(marketing_analyst, context=context)
        content_creator_task = tasks.content_creation(content_creator, context=context)
        SEO_specialist_task = tasks.SEO(SEO_specialist, context=context)
        return {
        "agents": {
            "manager": AgentModel(role=manager.role, goal=manager.goal, backstory=manager.backstory),
            "marketing_analyst": AgentModel(role=marketing_analyst.role, goal=marketing_analyst.goal, backstory=marketing_analyst.backstory),
            "content_creator": AgentModel(role=content_creator.role, goal=content_creator.goal, backstory=content_creator.backstory),
            "SEO_specialist": AgentModel(role=SEO_specialist.role, goal=SEO_specialist.goal, backstory=SEO_specialist.backstory),
            },
        "tasks":{
            "manager_task": TaskModel(description=manager_task.description, agentName=manager_task.agent.role),
            "marketing_analyst_task": TaskModel(description=marketing_analyst_task.description, agentName=marketing_analyst_task.agent.role),
            "content_creator_task": TaskModel(description=content_creator_task.description, agentName=content_creator_task.agent.role),
            "SEO_specialist_task": TaskModel(description=SEO_specialist_task.description, agentName=SEO_specialist_task.agent.role),
            }
        }
    except Exception as e:
        print(e)
 
@app.post('/edit-agent-info')   
def editAgentInfo(agentContent: AgentModel = Body(...),taskContent: TaskModel = Body(...)):
    try:
        if agentContent:
            agent_name = agentContent.role
            agent_goal = agentContent.goal
            agent_backstory = agentContent.backstory
            print(agent_name, agent_goal, agent_backstory)
            
            
        if taskContent:
            task_description = taskContent.description
            task_agent = taskContent.agentName
            
            print(task_description, task_agent)
            
            
        return {"result": "Task info updated"}
    
    except Exception as e:
        print(e)