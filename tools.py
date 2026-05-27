from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# TAVILY API KEY SETUP
# =========================

TAVILY_KEYS = [k.strip() for k in os.getenv("TAVILY_API_KEYS").split(",")]


def tavily_search_with_failover(query: str):
    last_error = None

    for key in TAVILY_KEYS:
        try:
            client = TavilyClient(api_key=key)
            return client.search(query=query, max_results=5)

        except Exception as e:
            print(f"Tavily key failed, trying next... {e}")
            last_error = e

    raise Exception(f"All Tavily API keys failed: {last_error}")


# =========================
# SEARCH TOOL
# =========================

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information."""

    results = tavily_search_with_failover(query)

    out = []

    for r in results["results"]:
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )

    return "\n----\n".join(out)


# =========================
# SCRAPER TOOL
# =========================

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL."""

    try:
        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"