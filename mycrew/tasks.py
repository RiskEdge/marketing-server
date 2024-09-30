from crewai import Task, Agent
from textwrap import dedent

from models.crewModels import ContextModel

class MarketingTasks:
    def marketing_management(self, agent: Agent, context: ContextModel) -> Task:
        return Task(
            description=dedent(f"""Drive business growth through strategic marketing initiatives for **{context.company_name}** which involves increasing brand visibility, generating leads, boosting sales and enhancing customer engagement, aligning with the company’s overall objectives and market positioning. Specific goals you should focus on include the following:
                - Implement comprehensive marketing strategies that align with company goals and target audiences.
                - Lead generation.
                - Content creation & Brand management
                - Market Research
            Use the details given as follows: \n\nCompany Website:**{context.company_website}**\n\nAbout Competitors: **{context.competitors_context}**\n\nCompany Services: **{context.services}**\n\nIndustry: **{context.industry}**\n\nAdditional Info: **{context.additional_info}** to create a detailed report."""),
            expected_output="Strategies to increase brand visibility and recognition, qualified leads and improve sales performance,customer engagement and satisfaction, optimized marketing performance with measurable ROI and effective management of marketing budgets and resources",
            agent=agent,
        )
        
    def marketing_analysis(
        self, agent: Agent, context: ContextModel) -> Task:
        return Task(
            description=dedent(f"""Optimize marketing strategies, improve campaign performance and increase ROI, provide actionable insights that align marketing efforts with business goals, identify growth opportunities and support data-driven decision-making for overall business success of **{context.company_name}**. Conducting competitor analysis of **{context.company_name}**'s competitors using **{context.competitors_context}** in **{context.industry}** industry for services such as **{context.services}** to evaluate their strengths, weaknesses and market positioning. You can also use **{context.additional_info}**."""),
            expected_output=f"A detailed report profiling top 4 competitors, including their offerings, target markets, strengths, and weaknesses. Identifying service gaps in **{context.services}** to enhance **{context.company_website}'s** value proposition. Refine marketing messages, sales strategies and branding based on competitor analysis. Provide data-driven insights on campaign performance, key metrics, trends and rankings of those competitors to improve ROI.",
            agent=agent,
        )
        
    def content_creation(self, agent: Agent, context: ContextModel) -> Task:
        return Task(
            description=dedent(f"""Produce high-quality, engaging content as **{context.content_type}** for **{context.company_name}** that drives traffic, boosts engagement and leads to conversions. Ensure content aligns with brand goals, optimized for search engines and resonates with the target audience for the following services: **{context.services}** in **{context.industry}** industry, delivering measurable business results like brand growth and lead generation. You can also use **{context.additional_info}**."""),
            expected_output=f"**{context.content_type}** for **{context.company_name}** to engage the target audience and meet business goals, includes clear service descriptions, posts on industry trends & case studies that showcase successful projects.",
            agent=agent,
        )
        
    def SEO(self, agent: Agent, context: ContextModel) -> Task:
        return Task(
            description=dedent(f"""Evaluate **{context.company_name}'s** website: **{context.company_website}** performance to identify issues affecting it's search engine visibility and rankings for the services such as **{context.services}** in **{context.industry}**.\n\nAnalyze technical aspects such as crawlability, site architecture, page speed and mobile optimization andbacklinks for quality. Assess the site's security and overall user experience.\n\nAdditional information: {context.additional_info}"""),
            expected_output="A detailed report highlighting key SEO issues and providing actionable recommendations to improve rankings, including fixing technical problems, optimizing content and enhancing site security for better search engine performance.",
            agent=agent,
        )
