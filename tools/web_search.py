from langchain.tools import tool
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    ArxivAPIWrapper,
    WikipediaAPIWrapper,
    GoogleTrendsAPIWrapper,
    GoogleScholarAPIWrapper,
)
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    ArxivQueryRun,
    WikipediaQueryRun,
    GoogleSearchRun,
    AskNewsSearch,
    OpenWeatherMapQueryRun,
    RedditSearchRun,
    SearxSearchRun,
)


# --- TOOL DEFINITIONS ---

@tool
def DuckDuckGo():
    """Perform web search using DuckDuckGo."""
    duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)
    return DuckDuckGoSearchRun(
        name="DuckDuckGoSearch",
        api_wrapper=duckduckgo_wrapper,
        description="Use this tool for general-purpose web searches when you need up-to-date or privacy-preserving results.",
    )

@tool
def Arxiv():
    """Perform academic paper search via Arxiv."""
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=500)
    return ArxivQueryRun(
        name="ArxivSearch",
        api_wrapper=arxiv_wrapper,
        description="Use this tool to search and summarize academic or scientific papers from Arxiv. Ideal for technical or research topics.",
    )

@tool
def Wikipedia():
    """Perform encyclopedia search via Wikipedia."""
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=500)
    return WikipediaQueryRun(
        name="WikipediaSearch",
        api_wrapper=wiki_wrapper,
        description="Use this tool for general factual or historical information from Wikipedia.",
    )

@tool
def GoogleSearch():
    """Perform web search using Google."""
    google_wrapper = GoogleSearchAPIWrapper()
    return GoogleSearchRun(
        name="GoogleSearch",
        api_wrapper=google_wrapper,
        description="Use this tool for broad and up-to-date web searches using Google. Ideal for news, websites, or general questions.",
    )

@tool
def GoogleScholar():
    """Perform academic search via Google Scholar."""
    scholar_wrapper = GoogleScholarAPIWrapper(top_k_results=5)
    return scholar_wrapper.as_tool(
        name="GoogleScholarSearch",
        description="Use this tool to find peer-reviewed research papers or academic publications from Google Scholar.",
    )

@tool
def GoogleTrends():
    """Analyze keyword popularity via Google Trends."""
    trends_wrapper = GoogleTrendsAPIWrapper()
    return trends_wrapper.as_tool(
        name="GoogleTrends",
        description="Use this tool to analyze trending search topics or compare keyword popularity across time or regions.",
    )

@tool
def AskNews():
    """Search current news headlines and articles."""
    return AskNewsSearch(
        name="AskNews",
        description="Use this tool to search for breaking news and recent media coverage on a topic.",
    )

@tool
def RedditSearch():
    """Search Reddit posts and comments."""
    return RedditSearchRun(
        name="RedditSearch",
        description="Use this tool to search Reddit posts and community discussions. Helpful for opinions or social sentiment.",
    )

@tool
def SearxSearch():
    """Perform privacy-friendly web search using Searx."""
    return SearxSearchRun(
        name="SearxSearch",
        description="Use this tool for privacy-respecting meta search results across multiple search engines (via Searx).",
    )

@tool
def Weather():
    """Query weather data via OpenWeatherMap."""
    return OpenWeatherMapQueryRun(
        name="WeatherQuery",
        description="Use this tool to get current or forecasted weather information for a given location.",
    )
