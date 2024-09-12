from crewai import Task, Agent
from textwrap import dedent

class MarketingTasks:
    def marketing_management(self, agent: Agent, topic) -> Task:
        return Task(
            description=dedent(f"""\
                Primary goal is to drive business growth by attracting potential clients, generating high-quality leads and building {topic} brand reputation in the market.
                Delegate marketing responsibilities to team members, monitor their progress and offer support when needed.
                Ensure the team stays focused and deliver taks on time with accuracy.
                Specific goals you should focus on include the following:
                - Increase office property sales and rentals.
                - Lead generation.
                - Customer engagement
                - Market analysis and adaptation
                - Optimize online presence
                - Track ROI on marketing efforts
                """),
            expected_output="A list of performance of each team member and their role in the team",
            agent=agent,
        )

        
    # def data_analysis(self, agent, topic):
    #     return Task(
    #         description=dedent("""\ 
                
    #                            """),
    #     )
        
    def competitor_analysis(
        self, agent: Agent, website: str , property_details: str = None
    ) -> Task:
        """Create a task to analyze competitors of a real estate website.

        Args:
            agent: The agent to assign this task to.
            website: The website to analyze.
            property_details: Optional details about the properties to analyze.

        Returns:
            A Task object with the description and agent set.
        """
        return Task(
            description=dedent(f"""\ 
                Explore real estate competitors that rent or sell office spaces.
                Extra details provided by user : {property_details}.
                
                Identify top 3 competitors and analyze their strategies, market positioning, and customer perception.
                
                Your final report MUST include BOTH all content about {website} and a detailed comparison to whatever competitors they have.
                """),
            expected_output='A full report of top 3 competitors listing their strategies and market performance with suggestions for the brand.',
            agent=agent
        )
        
    def content_creation(self, agent: Agent, platform: str) -> Task:
        return Task(
            description=dedent(f"""\ 
                Create a compelling content for {platform}.
                
                Ensure the message aligns with the brand's voice and speaks to the target audience's needs and preferences.
            """),
            expected_output="An SEO rich article/post about the company or promotional content for offic space rentals.",
            agent=agent
        )
        
    def SEO(self, agent: Agent, topic) -> Task:
        return Task(
            description=dedent(f"""\
                Identify key search terms related to real estate and rental office spaces for {topic}.
                
                For content optimization collaborate with Content Creator to optimize blog posts, property listings, social media content and other content for search engines.
                """),
            expected_output="A list of top performing keywords that can be included in blog posts and articles for different platforms.",
            agent=agent
        )
