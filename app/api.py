from dotenv import load_dotenv
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from fastapi import FastAPI,  Form
from fastapi.middleware.cors import CORSMiddleware

from crewai import Crew

from mycrew.agents import MarketingAgents
from mycrew.tasks import MarketingTasks

from models.crewModels import AgentModel, TaskModel, ContextModel, MarketingModel, ContentModel, InfoModel

from supabase import create_client, Client


app = FastAPI()

load_dotenv()


# LOGGER-----------------------------------------------------
# Create logs directory
os.makedirs("logs", exist_ok=True)

# Setup monthly rotating logs
log_handler = TimedRotatingFileHandler(
    filename="logs/app.log",
    when="midnight",
    interval=30,
    backupCount=6,
    encoding='utf-8',
    utc=True
)
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("fastapi_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)
logger.propagate = False

#-------------------------------------------------------------

origins = [
    "https://marketing-app.riskedgesolutions.com",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


tasks = MarketingTasks()

async def getAgentFromDB(agent_name):
    logger.info(f"Fetching agent '{agent_name}' from Supabase.")
    supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])  
    try:
        data = (
            supabase.table("agents")
            .select("edited_goal, edited_backstory")
            .eq("agent_name", agent_name)
            .execute()
            .data[0]
        )
        logger.debug(f"Agent data: {data}")
        return data
    except Exception as e:
        logger.error(f"Error fetching agent from DB: {e}")
        print(f"Error fetching agent from DB: {e}")
        raise
    
async def getTaskFromDB(task_name):
    logger.info(f"Fetching task '{task_name}' from Supabase.")
    supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])  
    try:
        data = (
            supabase.table("tasks")
            .select("edited_description, edited_expected_output")
            .eq("task_name", task_name)
            .execute()
            .data[0]
        )
        logger.debug(f"Task data: {data}")
        return data
    except Exception as e:
        logger.error(f"Error fetching task from DB: {e}")
        print(f"Error fetching task from DB: {e}")
        raise

@app.get('/')
async def index() -> dict:
    logger.info("Index route accessed.")
    return {"message" : 'Hello World'}

@app.post('/marketing-analyst')
# async def formInput(context: ContextModel = Body(...)):
async def marketingAnalyst(context: MarketingModel = Form(...)):
    try:
        logger.info("Received request at /marketing-analyst endpoint.")
        agents = MarketingAgents(model=context.llm)
        
        # agent_info = await getAgentFromDB("Marketing Analyst")
        # task_info = await getTaskFromDB("Marketing Analysis")

        # marketing_analyst = agents.marketing_analyst(goal=agent_info["edited_goal"], backstory=agent_info["edited_backstory"])
        # marketing_analyst_task = tasks.marketing_analysis(agent=marketing_analyst, description=task_info["edited_description"], expected_output=task_info["edited_expected_output"], context=context)
        marketing_analyst = agents.marketing_analyst()
        marketing_analyst_task = tasks.marketing_analysis(marketing_analyst, context)
        
        marketing_analysis_crew = Crew(
        agents = [marketing_analyst],
        tasks = [marketing_analyst_task],
        verbose=True,
        full_output=True,
        # planning=True,
        )
        
        result = marketing_analysis_crew.kickoff()
        logger.info("Crew task executed successfully.")
        logger.debug(f"Crew result: {result}")
        
        
        return {"result": result,
                "status": 200} 
   
    except Exception as e:
        print(e)
        logger.exception("Error in /marketing-analyst endpoint:")
        return {"status": 400,
                "message": f"Couldn't generate response: {e}"}

@app.post('/seo-specialist')
async def seoSpecialist(context: ContextModel = Form(...)):
    try:
        # print(context)
        logger.info("Received request at /seo-specialist endpoint.")
        agents = MarketingAgents(model=context.llm)
        
        
        # agent_info = await getAgentFromDB("SEO Specialist")
        # task_info = await getTaskFromDB("SEO")
        
        # SEO_specialist = agents.SEO_specialist(goal=agent_info["edited_goal"], backstory=agent_info["edited_backstory"])
        # SEO_specialist_task = tasks.SEO(agent=SEO_specialist, description=task_info["edited_description"], expected_output=task_info["edited_expected_output"], context=context)
        
        SEO_specialist = agents.SEO_specialist()
        SEO_specialist_task = tasks.SEO(SEO_specialist, context)
        
        seo_crew = Crew(
        agents = [SEO_specialist],
        tasks = [ SEO_specialist_task],
        verbose=True,
        full_output=True,
        # planning=True,
        )
        result = seo_crew.kickoff()
        logger.info("Crew task executed successfully.")
        logger.debug(f"Crew result: {result}")
        
        # print("RESULT: ", result)
        return {"result": result,
                "status": 200} 
    except Exception as e:
        print(e)
        logger.exception("Error in /seo-specialist endpoint:")
        return {"status": 400,
                "message": f"Couldn't generate response: {e}"}
        
@app.post('/content-writer')
async def contentWriter(context: ContentModel = Form(...)):
    try:
        # print(context)
        logger.info("Received request at /content-writer endpoint.")
        agents = MarketingAgents(model=context.llm, temp=context.creativity)
        
        
        # agent_info = await getAgentFromDB("Content Writer")
        # task_info = await getTaskFromDB("Content Writing")
        
        # content_creator = agents.content_creator(goal=agent_info["edited_goal"], backstory=agent_info["edited_backstory"])
        # content_creator_task = tasks.content_creation(agent=content_creator, description=task_info["edited_description"], expected_output=task_info["edited_expected_output"], context=context)
        
        content_creator = agents.content_creator()
        content_creator_task = tasks.content_creation(content_creator, context)
        
        content_creation_crew = Crew(
        agents = [content_creator],
        tasks = [content_creator_task],
        verbose=True,
        full_output=True,
        planning=True,
        )
        result = content_creation_crew.kickoff()
        logger.info("Crew task executed successfully.")
        logger.debug(f"Crew result: {result}")
        
        return {"result": result,
                "status": 200} 
    
    except Exception as e:
        print(e)
        logger.exception("Error in /content-writer endpoint:")
        return {"status": 400,
                "message": f"Couldn't generate response: {e}"}
        

# @app.post('/agents-info')
@app.post('/agents-info')
# def sendAgentInfo():
def sendAgentInfo(context: InfoModel = Form(...)):
    try:
        logger.info("Fetching all agent and task data from Supabase.")
        print(context)
        
        marketing_data = {field: getattr(context, field) for field in MarketingModel.model_fields}
        content_data = {field: getattr(context, field) for field in ContentModel.model_fields}
        
        marketing_context = MarketingModel(**marketing_data)
        content_context = ContentModel(**content_data)
        
        agents = MarketingAgents(model="ChatGPT")
        tasks = MarketingTasks()

        # AGENTS
        marketing_analyst = agents.marketing_analyst()
        content_creator = agents.content_creator()
        SEO_specialist = agents.SEO_specialist()
        
        marketing_analyst_task = tasks.marketing_analysis(marketing_analyst, context=marketing_context)
        content_creator_task = tasks.content_creation(content_creator, context=content_context)
        SEO_specialist_task = tasks.SEO(SEO_specialist, context=marketing_context)
        
        logger.info("Returning structured agent and task objects.")
        
        return {
             "agents": {
                "marketing_analyst": AgentModel(role=marketing_analyst.role, goal=marketing_analyst.goal, backstory=marketing_analyst.backstory),
                "content_creator": AgentModel(role=content_creator.role, goal=content_creator.goal, backstory=content_creator.backstory),
                "SEO_specialist": AgentModel(role=SEO_specialist.role, goal=SEO_specialist.goal, backstory=SEO_specialist.backstory),
                },
            "tasks":{
                "marketing_analyst_task": TaskModel(task_name='Marketing Analysis', description=marketing_analyst_task.description, agentName=marketing_analyst_task.agent.role),
                "content_creator_task": TaskModel(task_name='Content Creation',description=content_creator_task.description, agentName=content_creator_task.agent.role),
                "SEO_specialist_task": TaskModel(task_name='SEO Analysis',description=SEO_specialist_task.description, agentName=SEO_specialist_task.agent.role),
                }}
    except Exception as e:
        print(e)
        logger.exception("Error while sending agent and task info:")
        return {"status": 400, "message": f"Error while fetching agent/task info: {e}"}
 
@app.put('/edit-agent-info')   
async def editSingleAgentInfo(agent_info: AgentModel = Form(...)):
    try:
        logger.info(f"Editing info for agent: {agent_info.role}")
        # Initialize Supabase client
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
        
        response = (
            supabase.table("agents")
            .update({"edited_goal": agent_info.goal, "edited_backstory": agent_info.backstory})
            .eq("agent_name", agent_info.role)
            .execute()
        )
        
        logger.debug(f"Update response: {response}")
        
        return {
            "status": 200,
            "response": response,
            "message": "Agent info updated successfully"
        }
    
    except Exception as e:
        print("Error while editing agent info:", e)
        logger.exception("Error while editing agent info:")
        return {
            "status": 400,
            "response": response,
            "message": f"Error while updating agent info: {e}"
        }
        
@app.put('/reset-agent-info')
async def resetAgentInfo(role: str = Form(...)):
    try:
        logger.info(f"Resetting info for agent: {role}")
        
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
        
        default_info = (
            supabase.table("agents")
            .select("default_goal, default_backstory").
            eq("agent_name", role)
            .execute()
            .data
        )[0]
        
        # print("Default info: ", default_info)
        logger.debug(f"Default agent info: {default_info}")
        
        response = (
            supabase.table("agents")
            .update({"edited_goal": default_info["default_goal"], "edited_backstory": default_info["default_backstory"]})
            .eq("agent_name", role)
            .execute()
        )
        
        return {
            "status": 200,
            "response": response,
            "message": "Agent info reset successful"
        }
    except Exception as e:
        print("Error while resetting agent info:", e)
        logger.exception(f"Error while resetting agent info:", e)
        return {
            "status": 400,
            "message": f"Error while resetting agent info: {e}"
        }   
        
@app.put('/edit-task-info')
async def editSingleTaskInfo(task_info: TaskModel = Form(...)):
    try:
        # print(task_info)
        logger.info(f"Editing task info: {task_info.task_name}")
        # Initialize Supabase client
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
        
        response = (
            supabase.table("tasks")
            .update({"edited_description": task_info.description})
            .eq("task_name", task_info.task_name)
            .execute()
        )
        
        logger.debug(f"Update response: {response}")
        
        return {
            "status": 200,
            "response": response,
            "message": "Task info updated successfully"
        }
    except Exception as e:
        print("Error while editing task info:", e)
        logger.exception("Error while editing task info:", e)
        return {
            "status": 400,
            "response": response,
            "message": f"Error while editing task info: {e}"
        }
        
@app.put('/reset-task-info')
async def resetTaskInfo(task_name: str = Form(...)):
    try:
        logger.info(f"Resetting task info for task: {task_name}")
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
        
        default_info = (
            supabase.table("tasks")
            .select("default_description").
            eq("task_name", task_name)
            .execute()
            .data
        )[0]
        
        # print("Default info: ", default_info)
        logger.debug(f"Default task info: {default_info}")
        
        response = (
            supabase.table("tasks")
            .update({"edited_description": default_info["default_description"],})
            .eq("task_name", task_name)
            .execute()
        )
        
        return {
            "status": 200,
            "response": response,
            "message": "Task info reset successful"
        }
    except Exception as e:
        print("Error while resetting task info:", e)
        logger.exception("Error while resetting task info:", e)
        return {
            "status": 400,
            "message": f"Error while resetting task info: {e}"
        }