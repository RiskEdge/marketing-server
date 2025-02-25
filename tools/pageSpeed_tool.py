import json
import os
from pydantic import BaseModel, Field
import requests
from crewai import Agent, Task
# from crewai.tools import tool
from langchain.tools import tool
from unstructured.partition.html import partition_html

# class UrlFormat(BaseModel):
#     website: str = Field("The url of the website whose insights are to be fetched.")

class PageSpeedTool():

    @tool("Google PageSpeed Insights")
    def analyze_website_seo(website: str) -> str:
        """Analyzes a website's SEO and performance using Google's PageSpeed Insights API."""

        pagespeed_api_key = os.environ["GOOGLE_PAGESPEED_API_KEY"]
        if pagespeed_api_key is None:
            raise ValueError("PAGESPEED_API_KEY environment variable not set.")

        base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            "url": website,
            "category": ["performance", "accessibility", "best-practices", "seo"],
            "strategy": "desktop",  # or "desktop"
            "key": pagespeed_api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            pagespeed_data = response.json()
            # print("PageSpeed Data: ", pagespeed_data)

            # Extract relevant SEO information (customize as needed)
            seo_metrics = {}
            try:
                lighthouse_result = pagespeed_data.get("lighthouseResult", {})
                # seo_metrics["overall_score"] = lighthouse_result.get("overall_score")
                # Example: Extracting specific SEO audits (customize)
                audits = lighthouse_result.get("audits", {})
                categories = lighthouse_result.get("categories", {})
                
                # Core Web Vitals (from loadingExperience and originLoadingExperience)
                for experience_type in ["loadingExperience", "originLoadingExperience"]:
                    experience_data = pagespeed_data.get(experience_type, {})
                    if experience_data:
                        seo_metrics[f"{experience_type}_overall_category"] = experience_data.get("overall_category")
                        metrics = experience_data.get("metrics", {})
                        for metric in ["FIRST_CONTENTFUL_PAINT", "LARGEST_CONTENTFUL_PAINT", "CUMULATIVE_LAYOUT_SHIFT", "FIRST_INPUT_DELAY"]:
                            if metric in metrics:
                                seo_metrics[f"{experience_type}_{metric}"] = metrics[metric].get("category")

                # Lighthouse Audits (Performance related)
                performance_audits = [
                    "speed-index", "first-contentful-paint", "largest-contentful-paint", "cumulative-layout-shift",
                    "interactive", "total-blocking-time", "max-potential-fid", "first-cpu-idle",
                    "estimated-input-latency", "server-response-time", "render-blocking-resources",
                    "uses-optimized-images", "uses-webp-images", "uses-text-compression", "uses-efficient-video-encoding",
                    "uses-minified-css", "uses-minified-javascript", "uses-combined-css", "uses-combined-javascript",
                    "uses-lazy-loading", "offscreen-images", "unoptimized-images", "efficient-compression",
                    "reduce-unused-css", "reduce-unused-javascript", "uses-http2", "uses-push-preload", "font-display",
                    "critical-request-chains", "bootup-time", "mainthread-work-breakdown", "long-tasks",
                    "js-execution-time", "first-meaningful-paint", "metric-weights"
                ]
                for audit_id in performance_audits:
                    if audit_id in audits:
                        seo_metrics[f"audit_{audit_id}_score"] = audits[audit_id].get("score")
                        if audits[audit_id].get("displayValue"):
                            seo_metrics[f"audit_{audit_id}_displayValue"] = audits[audit_id].get("displayValue")

                # Lighthouse Categories (Overall scores)
                for category_id in ["performance", "accessibility", "best-practices", "seo", "pwa"]:
                    if category_id in categories:
                        seo_metrics[f"category_{category_id}_score"] = categories[category_id].get("score")

                # Other relevant fields
                seo_metrics["final_url"] = lighthouse_result.get("finalUrl")
                seo_metrics["requested_url"] = lighthouse_result.get("requestedUrl")
                seo_metrics["fetch_time"] = lighthouse_result.get("fetchTime")

                #SEO specific audits
                seo_audits = ["document-title", "meta-description", "http-status-code", "link-text", "is-on-https", "canonical", "viewport", "hreflang", "robots-txt", "sitemap", "structured-data", "font-display"]
                for audit_id in seo_audits:
                    if audit_id in audits:
                        seo_metrics[f"audit_{audit_id}_score"] = audits[audit_id].get("score")
                        if audits[audit_id].get("displayValue"):
                            seo_metrics[f"audit_{audit_id}_displayValue"] = audits[audit_id].get("displayValue")
                
                
                print("SEO Metrics:\n\n", seo_metrics)
            
            
                # seo_metrics["meta-description"] = audits.get("meta-description", {}).get("details", {}).get("items", [{}])[0].get("description")
                # seo_metrics["title"] = audits.get("title", {}).get("details", {}).get("items", [{}])[0].get("description")
                # ... extract other SEO-related audits ...
            except (KeyError, IndexError) as e:  # Handle cases where the data might be missing
                return f"Error extracting SEO data: {e}. Check the PageSpeed Insights response."
            
            # Format the string:
            output_string = f"SEO Analysis for {website}:\n"
            for metric, value in seo_metrics.items():
                output_string += f"- {metric}: {value}\n"
                
            print("Output string from PageSpeed API: ", output_string)

            return output_string  # Return the formatted string

        except requests.exceptions.RequestException as e:
            return f"Error fetching PageSpeed Insights data: {e}"

