from crewai import Task, Agent
from textwrap import dedent

class MarketingTasks:
    def marketing_management(self, agent: Agent, topic:str = None) -> Task:
        return Task(
            description=dedent(f"""Primary goal is to drive business growth by attracting potential clients, generating high-quality leads and building {topic} brand awareness in the market. Lead your marketing team.
Specific goals you should focus on include the following:
                - Implement marketing strategies to Increase office property sales and rentals.
                - Lead generation.
                - Customer engagement
                - Market Research and competitors’ offerings
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
        self, agent: Agent, website: str = None , property_details: str = None
    ) -> Task:
        """Create a task to analyze competitors of a real estate website.

        Args:
            agent: The agent to assign this task to.
            website: The website to analyze.
            property_details: Optional details about the properties to analyze.

        Returns:
            A Task object with the description and agent set.
            
        PROERTY DETAILS
        """
        return Task(
            description=dedent(f"""Identify direct competitors in the office and co working spaces.
Extra details provided by user : {property_details}. Identify how competitors position themselves in the market and assess their target audience. Examine competitors’ branding efforts, including their online presence.
                             
Your final report MUST include BOTH, all content about {website} and a detailed comparison of the competitors they have.

                """),
            expected_output='A detailed report profiling key competitors, their offerings, target markets, strengths, and weaknesses. Identification of gaps in competitors’ services that can be leveraged to differentiate and enhance your firm’s value proposition. Refining your marketing messages, sales strategies, and branding efforts based on competitors strengths and weaknesses.',
            agent=agent,
        )
        
    def content_creation(self, agent: Agent, platform: str = None) -> Task:
        return Task(
            description=dedent(f"""Create a compelling content for Maximize consumer engagement{platform}.
                
Ensure the message aligns with the brand's voice and speaks to the target audience's needs and preferences.

            """),
            expected_output="An SEO rich article/post about the company services providing office spaces and co working spaces and advantages or promotional content and real life examples how people will benefit from these services.",
            agent=agent,
        )
        
    def SEO(self, agent: Agent, topic = None) -> Task:
        return Task(
            description=dedent(f"""Focus on long-tail keywords that are specific to your offerings related to real estate rental office spaces and co working spaces for {topic}.
Optimize meta titles, descriptions, headers, and URLs with these keywords to boost search engine visibility.
For content optimization collaborate with Content Creator to optimize blog posts, property listings, social media content 
                """),
            expected_output="Improve search engine rankings and organic traffic using relevant keywords, A list of top performing keywords and content that can be included in blog posts, social media posts on LinkedIn and twitter platforms",
            agent=agent,
        )
