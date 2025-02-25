import os

from crewai import Agent
from textwrap import dedent

from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from tools.pageSpeed_tool import PageSpeedTool

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm(model: str, temp: float = 0):
    """
    Returns an initialized LLM object based on the provider and model.
    """
    if model.lower() == "chatgpt":
        return ChatOpenAI(model='gpt-4o', temperature=temp, api_key=os.environ["OPENAI_API_KEY"])
    
    elif model.lower() == "gemini":
        return ChatGoogleGenerativeAI(model='models/gemini-1.5-flash', temperature=temp, google_api_key=os.environ["GOOGLE_API_KEY"])
    
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

class MarketingAgents:
    def __init__(self, model: str, temp: float = 0):
        self.llm = get_llm(model, temp)
        
    def marketing_manager(self):
        return Agent(
            role="Marketing Manager",
            goal=dedent("""Understand the context and assign the tasks to the team members."""),
            backstory=dedent("""As a Marketing Manager, I provide clear instructions and set expectations tailored to each agent’s role, ensuring that each team member understands their responsibilities in delivering high-quality results. 
            Marketing Analyst: Your primary task is to track and analyze key performance metrics highlighting insights and competitor analysis.
            Content Creator: Focus on producing high-quality content that reflects the brand.
            SEO Specialist: You are responsible for optimizing our content for search engines. Provide a keyword list and ensure that all content is aligned with our SEO strategy. Auditing the website will help us identify any technical issues."""),
            allow_delegation=True,
            llm=self.llm,
            verbose=True
        )
        
    def marketing_analyst(self):
        return Agent(
            role="Marketing Analyst",
            
            goal=dedent("""Analyze market trends, competitor strategies, and digital presence to develop high-performing marketing strategies for the client. Conduct a thorough competitor and market analysis, evaluating key players' positioning, content strategies, and engagement metrics across platforms like Instagram, LinkedIn, and Twitter. Identify opportunities to optimize branding, improve customer engagement, and maximize ROI. Provide actionable insights that align with the client’s business goals, ensuring a data-driven, competitive edge."""),
            
            backstory=dedent("""You are an expert Marketing Analyst with deep expertise in market research, digital strategy, and competitor intelligence. You have a strong grasp of industry trends, customer behavior, and emerging digital marketing techniques. Your skill set includes social media analytics, SEO, SEM, email marketing, and performance tracking. You specialize in analyzing competitors' branding, content, and engagement tactics across Instagram, LinkedIn, Twitter, and other digital platforms. By leveraging data insights, you craft strategies that enhance brand positioning, optimize ad spend, and drive targeted engagement. Your role is to translate raw data into actionable marketing plans that help clients outperform competitors and grow their digital footprint."""),
            
            tools=[
                # BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,   
                SearchTools.search_instagram,   
                SearchTools.search_linkedin,   
                SearchTools.search_twitter, 
                PageSpeedTool.analyze_website_seo  
            ],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )
    
    def content_creator(self):
        return Agent(
            role="Content Creator",
            goal=dedent("""Produce high-quality, engaging and strategic content that drives audience engagement, improves search engine rankings and generate high-quality leads. Support business objectives and deliver measurable results by optimizing content across various channels to increase visibility and reach broader audience. Ensure all content aligns with the brand’s voice, values and visual identity."""),
            
            backstory=dedent("""You are a professional in developing conversion driven content. Expert in SEO including keyword research, on-page optimization and content structure to enhance visibility and rankings on search engines. Expertise in creating and managing content for various social media platforms, including knowledge of platform-specific best practices and tools. You have strong analytical skills utilizing tools such as Google Analytics and social media insights to evaluate content performance, measure effectiveness, and make data-driven decisions."""),
            tools=[
                # BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,   
            ],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )
        
    # def SEO_specialist(self):
    #     return Agent(
    #         role="SEO Specialist", 
    #         goal=dedent("""Conduct client's website audit to identify and rectify technical, on-page and off-page SEO issues that may be hindering the website's organic search performance. Drive organic traffic and improve search engine rankings."""),
            
    #         backstory=dedent("""You are proficient in conducting technical SEO audit, reviewing the site's crawlability and indexability by search engines. Assess the site's architecture, ensuring a well-organized URL structure and internal linking. Site performance, including loading speed and mobile responsiveness, is also examined, along with checking for the correct implementation of structured data like schema markup. Experienced in analyzing competitors SEO strategies and identifying opportunities for improvement."""),
    #         tools=[
    #             # BrowserTools.scrape_and_summarize_website,
    #             SearchTools.search_internet,   
    #         ],
    #         allow_delegation=False,
    #         llm=self.llm,
    #         verbose=True
    #         )
    
    def SEO_specialist(self):
        agent =  Agent(
            role="SEO Specialist",
            goal="""Analyze a website’s performance using Google PageSpeed API and provide SEO recommendations.\nConduct client's website audit to identify and rectify technical, on-page and off-page SEO issues that may be hindering the website's organic search performance. Drive organic traffic and improve search engine rankings.""",
            backstory="""You are proficient in conducting technical SEO audit, reviewing the site's crawlability and indexability by search engines. 
            Assess the site's architecture, ensuring a well-organized URL structure and internal linking, site performance, including loading speed and mobile responsiveness, is also examined, along with checking for the correct implementation of structured data like schema markup. 
            Experienced in analyzing competitors SEO strategies and identifying opportunities for improvement.
            An expert in web performance and SEO optimization, leveraging AI to analyze and improve website rankings.""",
            tools=[PageSpeedTool.analyze_website_seo,
                   SearchTools.search_internet],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
            )
        # print(agent)
        return agent