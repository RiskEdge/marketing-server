import json
import os

import requests
from langchain.tools import tool


class SearchTools():

  @tool("Search internet")
  def search_internet(query):
    """Useful to search the internet about a given topic and return relevant
    results."""
    return SearchTools.search(query)

  @tool("Search instagram")
  def search_instagram(query):
    """Useful to search for instagram post about a given topic/comapny and return relevant
    results."""
    query = f"site:instagram.com {query}"
    return SearchTools.search(query)
  
  @tool("Search linkedin")
  def search_linkedin(query):
    """Useful to search for linkedin post about a given topic/company and return relevant
    results."""
    query = f"site:linkedin.com {query}"
    return SearchTools.search(query)
  
  @tool("Search twitter")
  def search_twitter(query):
    """Useful to search for twitter post about a given topic/company and return relevant
    results."""
    query = f"site:twitter.com {query}"
    return SearchTools.search(query)
  
  

  def search(query, n_results=3):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("Response from SERP API: ", response.json())
    results = response.json()['organic']
    stirng = []
    for result in results[:n_results]:
      try:
        stirng.append('\n'.join([
            f"Title: {result['title']}", 
            # f"Link: {result['link']}",
            f"Snippet: {result['snippet']}", "\n-----------------"
        ]))
      except KeyError:
        next

    content = '\n'.join(stirng)
    # print("Search tools content: \n\n", content)
    return f"\nSearch result: {content}\n"