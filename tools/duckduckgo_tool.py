from crewai_tools import BaseTools, WebsiteSearchTool
from langchain_community.tools import DuckDuckGoSearchRun

import requests
from bs4 import BeautifulSoup
import urllib.parse

class Ddgs_Search(BaseTools):
   pass
