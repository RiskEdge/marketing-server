from dotenv import load_dotenv
import os

from fastapi import FastAPI,  Form
from fastapi.middleware.cors import CORSMiddleware

from crewai import Crew

from mycrew.agents import MarketingAgents
from mycrew.tasks import MarketingTasks

from models.crewModels import AgentModel, TaskModel, ContextModel, MarketingModel, ContentModel, InfoModel

from supabase import create_client, Client


app = FastAPI()

load_dotenv()

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
    supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])  
    return (
            supabase.table("agents").
            select("edited_goal, edited_backstory")
            .eq("agent_name", agent_name)
            .execute()
            .data
            )[0]
    
async def getTaskFromDB(task_name):
    supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])  
    return (
            supabase.table("tasks").
            select("edited_description, edited_expected_output")
            .eq("task_name", task_name)
            .execute()
            .data
            )[0]

@app.get('/')
async def index() -> dict:
    return {"message" : 'Hello World'}

@app.post('/marketing-analyst')
# async def formInput(context: ContextModel = Body(...)):
async def marketingAnalyst(context: MarketingModel = Form(...)):
    try:
        agents = MarketingAgents(model=context.llm)
        
        agent_info = await getAgentFromDB("Marketing Analyst")
        task_info = await getTaskFromDB("Marketing Analysis")

        marketing_analyst = agents.marketing_analyst(goal=agent_info["edited_goal"], backstory=agent_info["edited_backstory"])
        marketing_analyst_task = tasks.marketing_analysis(agent=marketing_analyst, description=task_info["edited_description"], expected_output=task_info["edited_expected_output"], context=context)
        
        marketing_analysis_crew = Crew(
        agents = [marketing_analyst],
        tasks = [marketing_analyst_task],
        verbose=True,
        full_output=True,
        planning=True,
        )
        
        result = marketing_analysis_crew.kickoff()
        return {"result": result,
                "status": 200} 
   
    except Exception as e:
        print(e)
        return {"status": 400,
                "message": f"Couldn't generate response: {e}"}

@app.post('/seo-specialist')
async def seoSpecialist(context: ContextModel = Form(...)):
    try:
        print(context)
        agents = MarketingAgents(model=context.llm)
        
        
        agent_info = await getAgentFromDB("SEO Specialist")
        task_info = await getTaskFromDB("SEO")
        
        SEO_specialist = agents.SEO_specialist(goal=agent_info["edited_goal"], backstory=agent_info["edited_backstory"])
        SEO_specialist_task = tasks.SEO(agent=SEO_specialist, description=task_info["edited_description"], expected_output=task_info["edited_expected_output"], context=context)
        
        seo_crew = Crew(
        agents = [SEO_specialist],
        tasks = [ SEO_specialist_task],
        verbose=True,
        full_output=True,
        planning=True,
        )
        result = seo_crew.kickoff()
        return {"result": result,
                "status": 200} 
    except Exception as e:
        print(e)
        return {"status": 400,
                "message": f"Couldn't generate response: {e}"}
        
@app.post('/content-writer')
async def contentWriter(context: ContentModel = Form(...)):
    try:
        print(context)
        agents = MarketingAgents(model=context.llm, temp=context.creativity)
        
        
        agent_info = await getAgentFromDB("Content Writer")
        task_info = await getTaskFromDB("Content Writing")
        
        content_creator = agents.content_creator(goal=agent_info["edited_goal"], backstory=agent_info["edited_backstory"])
        content_creator_task = tasks.content_creation(agent=content_creator, description=task_info["edited_description"], expected_output=task_info["edited_expected_output"], context=context)
        
        content_creation_crew = Crew(
        agents = [content_creator],
        tasks = [content_creator_task],
        verbose=True,
        full_output=True,
        planning=True,
        )
        result = content_creation_crew.kickoff()
        return {"result": result,
                "status": 200} 
    
    except Exception as e:
        print(e)
        return {"status": 400,
                "message": f"Couldn't generate response: {e}"}
        

@app.post('/agents-info')
def sendAgentInfo(context: InfoModel = Form(...)):
    try:
        # Extract and create context models
        marketing_context = MarketingModel(**{field: getattr(context, field) for field in MarketingModel.model_fields})
        content_context = ContentModel(**{field: getattr(context, field) for field in ContentModel.model_fields})

        # Initialize Supabase client
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

        # Fetch data from Supabase
        agent_table_response, task_table_response = (
            supabase.table(table)
            .select("*")
            .execute()
            .data for table in ["agents", "tasks"]
        )

        agents = MarketingAgents(model="ChatGPT")
        tasks = MarketingTasks()

        # Map agent names to creation functions
        agent_creation_funcs = {
            "Marketing Analyst": agents.marketing_analyst,
            "Content Writer": agents.content_creator,
            "SEO Specialist": agents.SEO_specialist
        }

        # Create agents
        agent_objects = {
            agent_response["agent_name"]: agent_creation_funcs[agent_response["agent_name"]](
                goal=agent_response["edited_goal"], 
                backstory=agent_response["edited_backstory"]
            ) 
            for agent_response in agent_table_response
            if agent_response["agent_name"] in agent_creation_funcs
        }

        # Map task names to task functions and contexts
        task_creation_funcs = {
            "Marketing Analysis": (tasks.marketing_analysis, marketing_context),
            "Content Writing": (tasks.content_creation, content_context),
            "SEO": (tasks.SEO, marketing_context)
        }

        # print(task_table_response[0])
        # Create tasks
        task_objects = {
            task_response["task_name"]: task_creation_funcs[task_response["task_name"]][0](
                agent=agent_objects[task_response["agent_name"]],
                description=task_response["edited_description"],
                expected_output=task_response["edited_expected_output"],
                context=task_creation_funcs[task_response["task_name"]][1]
            )
            for task_response in task_table_response
            if task_response["task_name"] in task_creation_funcs
        }
        

        return {
            "agents": {name: AgentModel(role=agent.role, goal=agent.goal, backstory=agent.backstory) for name, agent in agent_objects.items()},
            "tasks": {name + " Task": TaskModel(task_name=name, description=task.description, agentName=task.agent.role) for name, task in task_objects.items()}
        }
    except Exception as e:
        print(e)
 
@app.put('/edit-agent-info')   
async def editSingleAgentInfo(agent_info: AgentModel = Form(...)):
    try:
        # Initialize Supabase client
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
        
        response = (
            supabase.table("agents")
            .update({"edited_goal": agent_info.goal, "edited_backstory": agent_info.backstory})
            .eq("agent_name", agent_info.role)
            .execute()
        )
        
        return {
            "status": 200,
            "response": response,
            "message": "Agent info updated successfully"
        }
    
    except Exception as e:
        print("Error while editing agent info:", e)
        return {
            "status": 400,
            "response": response,
            "message": f"Error while updating agent info: {e}"
        }
        
@app.put('/reset-agent-info')
async def resetAgentInfo(role: str = Form(...)):
    try:
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
        
        default_info = (
            supabase.table("agents")
            .select("default_goal, default_backstory").
            eq("agent_name", role)
            .execute()
            .data
        )[0]
        
        print("Default info: ", default_info)
        
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
        return {
            "status": 400,
            "message": f"Error while resetting agent info: {e}"
        }   
        
@app.put('/edit-task-info')
async def editSingleTaskInfo(task_info: TaskModel = Form(...)):
    try:
        print(task_info)
        # Initialize Supabase client
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
        
        response = (
            supabase.table("tasks")
            .update({"edited_description": task_info.description})
            .eq("task_name", task_info.task_name)
            .execute()
        )
        
        return {
            "status": 200,
            "response": response,
            "message": "Task info updated successfully"
        }
    except Exception as e:
        print("Error while editing task info:", e)
        return {
            "status": 400,
            "response": response,
            "message": f"Error while editing task info: {e}"
        }
        
@app.put('/reset-task-info')
async def resetTaskInfo(task_name: str = Form(...)):
    try:
        supabase: Client = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
        
        default_info = (
            supabase.table("tasks")
            .select("default_description").
            eq("task_name", task_name)
            .execute()
            .data
        )[0]
        
        print("Default info: ", default_info)
        
        response = (
            supabase.table("tasks")
            .update({"edited_description": default_info["default_description"],})
            .eq("task_name", task_name)
            .execute()
        )
        
        return {
            "status": 200,
            "response": response,
            "message": "Agent info reset successful"
        }
    except Exception as e:
        print("Error while resetting task info:", e)
        return {
            "status": 400,
            "message": f"Error while resetting task info: {e}"
        }