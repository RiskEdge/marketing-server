from crewai import Task, Agent
from textwrap import dedent

from tools.pageSpeed_tool import PageSpeedTool

from models.crewModels import ContextModel, ContentModel, MarketingModel

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
        
    def marketing_analysis(self, agent: Agent, context) -> Task:
    # def marketing_analysis(self, agent: Agent, context: MarketingModel) -> Task:
        return Task(
            description=dedent(f"""Analyze the competitive landscape and market positioning of {context.company_name} within the {context.industry} industry. Conduct a deep dive competitor analysis using with the following context: {context.competitors_context}, evaluating their branding, marketing strategies, customer engagement, and social media presence (Instagram, LinkedIn, Twitter, etc.). Identify strengths, weaknesses, content trends, and service gaps in {context.services} to uncover opportunities for differentiation. Provide data-driven insights to refine marketing campaigns, sales strategies, and content positioning. Incorporate {context.additional_info} (if any) to enhance the analysis and optimize the marketing roadmap for business growth."""),
            expected_output=f"""A comprehensive competitor analysis report profiling the top 3 competitors, detailing their offerings, target audience, branding strategy, digital marketing performance, and engagement metrics across social platforms. A list of service gaps in {context.services}, highlighting opportunities for {context.company_website} to enhance its value proposition. Deliver key insights on industry trends, competitor rankings, and customer preferences, providing actionable recommendations to optimize marketing campaigns, refine messaging, improve lead generation, and maximize ROI.""",
            agent=agent,
        )
        
    # def content_creation(self, agent: Agent, context: ContentModel) -> Task:
    #     return Task(
    #         description=dedent(f"""Produce high-quality, engaging content as **{context.content_type}** with the topic **{context.topic}** for **{context.company_name}** that drives traffic, boosts engagement and leads to conversions. Ensure content aligns with brand goals, optimized for search engines and resonates with the target audience for the following services: **{context.services}** in **{context.industry}** industry, delivering measurable business results like brand growth and lead generation. You can also use **{context.additional_info}**."""),
    #         expected_output=f"**{context.content_type}** on **{context.topic}** for **{context.company_name}** to engage the target audience and meet business goals, includes clear service descriptions, posts on industry trends & case studies that showcase successful projects.",
    #         agent=agent,
    #     )
    
    # def content_creation(self, agent: Agent, context: ContentModel) -> Task:
    def content_creation(self, agent: Agent, context) -> Task:
        return Task(
            description = dedent(f"""
                    Craft a **{context.content_type}** on **{context.topic}** for **{context.company_name}** ({context.company_website}) that aligns with the brand’s vision and engages the target audience in the **{context.industry}** industry.

                    ### **Requirements:**
                    - **Tone & Style:** Ensure the content reflects the following style(s): **{context.tags}** (e.g., Funny, Engaging, Controversial, Descriptive, etc.).
                    - **SEO Optimization:** Use best practices for keyword placement and readability.
                    - **Creativity Level:** Adjust writing creativity to **{context.creativity}** to match the brand's identity.
                    - **Service Integration:** Clearly highlight services (**{context.services}**) if provided.
                    - **Industry Trends & Case Studies:** Incorporate relevant insights, examples, and business cases.
                    - **Additional Information:** Use **{context.additional_info}** for enhanced relevance.

                    **Goal:** Create impactful content that boosts brand awareness, engagement, and conversions.
                    """),
            expected_output = dedent(f"""
                    A **{context.content_type}** on **{context.topic}** for **{context.company_name}**, crafted to reflect the selected tone(s): **{context.tags}**.
                    The output should:
                    - **Capture the desired tone** (e.g., Funny, Descriptive, Engaging, Controversial, etc.).
                    - **Provide value** through insights, trends, and case studies.
                    - **Clearly articulate services** (**{context.services}** if applicable).
                    - **Be optimized for SEO**, including headings, keywords, and readability.
                    - **Engage the audience** with storytelling, data, or persuasive elements.
                    - **Align with business goals**, enhancing brand authority and conversions.
                    
                    The final content should be **polished, engaging, and ready for publication**."""),
            agent=agent,
        )
        
    def SEO(self, agent: Agent, context) -> Task:
    # def SEO(self, agent: Agent, context: ContextModel) -> Task:
        return Task(
            description=dedent(f"""For the technical SEO audit of **{context.company_name}**'s website use Google PageSpeed API to analyze the website insights: **{context.company_website}**. The checklist typically includes the following:\n\nCheck if an XML sitemap is present and if it's updated regularly.\nVerify the presence and correctness of the robots.txt file.\nCheck if the website has implemented rel=canonical tags to avoid duplicate content issues.\nVerify that the website returns appropriate HTTP status codes for all pages.\nCheck if the website has implemented proper redirects (301 redirects for permanent redirects and 302 redirects for temporary redirects) for any moved or deleted pages.\nVerify that the website has a logical and consistent URL structure.\nCheck the size of web pages and images to ensure they load quickly.\nVerify that the website is mobile-friendly and has a responsive design.\nCheck the website's load time and identify any issues that could be causing slow load times.\nVerify that the website has analytics and tracking code implemented correctly.\n\nAdditional information: {context.additional_info}"""),
            expected_output="A detailed report highlighting key SEO issues and providing actionable recommendations to improve rankings, including fixing technical problems, optimizing content and enhancing site security for better search engine performance.",
            agent=agent,
            # tools=[pagespeed_tool],
        )

