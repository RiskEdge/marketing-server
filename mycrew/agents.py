import os

from crewai import Agent
from textwrap import dedent

from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools

from langchain_openai import ChatOpenAI

class MarketingAgents:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.environ['OPENAI_API_KEY']
        )
        
    def marketing_manager(self):
        return Agent(
            role="Marketing Manager",
            goal=dedent("""\ 
                        Provide leadership and directions, make sure the team is focused on driving property sales, increasing brand awareness and generating leads."""),
            backstory=dedent("""\
                As the Cheif Marketing Manager, you have over 20 years of experience in real estate marketing.
                You understand the importance of relationship-building and brand management.
                You have a strategic mindset and you're motivated by the challenge of keeping the company ahead of market trends.
                """),
            allow_delegation=True,
            llm=self.llm,
            verbose=True
        )
        
    def data_analyst(self):
        return Agent(
            role="Data Analyst",
            goal=dedent("""\ 
                    Provide insights that drive data-driven decision-making.
                    Analyze data from competitors, analysze market trends, customer behaviors.
                    Provide actionable insights to improve lead generation.
                    """),
            backstory=dedent("""\
            You are a data mastermind behind company's marketing success.
            You are an expert in uncovering hidden patterns that significantly boost property sales.
            You love to dive deep into numbers to uncover trends that others might miss. 
            For you every marketing campaign is a puzzle to solve and data is the key.
            """),
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,   
            ],
            allow_delegation=False,
            llm=self.llm,
            verbose=False
        )
            
    def competitor_analyst(self):
        return Agent(
            role="Competitor Analyst",
            goal=dedent("""\
                Monitor, analyze and provide insights on competitor's activities, strategies and market positioning.
                """),
            backstory=dedent("""\ 
                  As a competitor analyst, you love being on the cutting edge of market intelligence, constantly learning about new trends and how competitors of rental office spaces are evolving.
                  Your analytical mindset pushes you to dig deeper into data and you enjoy the challenge of translating that data into actionable insight the directly influence the company's success.           
                """),
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet
            ],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )
    
    def content_creator(self):
        return Agent(
            role="Content Creator",
            goal=dedent("""\
                Develop compelling content for various platforms, including social media, email campaigns, blog posts and website content.
                The content aligns with the brand's voice and speaks to the target audience's needs and preferences. 
                """),
            backstory=dedent("""\
                You are a professional content creator and you believe that every property has a story.
                You goal is to tell that in a way that resonates with buyers.
                You are driven by the challenge of turning a simple listing into a narrative that speaks to the lifestyle and emotional aspirations of prospective clients.
                """),
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,   
            ],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )
        
    def SEO_specialist(self):
        return Agent(
            role="SEO Specialist", 
            goal=dedent("""\
                Ensure the real estate comapany's website, property listings and content are easily discoverable online.
                The website is optimized to rank higher in search engine results, increasing organic traffic and improving lead generation.
                Ensure that the content remains visible when potential clients search for relevant properties.
                         """),
            backstory=dedent("""\
                As an SEO specialist you thrive on the challenge of understanding ever-changing search engine algorithms and staying ahead of the competition.
                You're data-driven and love the process of analyzing search trends, optimizing content and watching your efforts to pay off in the form of higher rankings and increased traffic.
                """),
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,   
            ],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
            )