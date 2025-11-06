from langchain.tools import tool
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    ArxivAPIWrapper,
    WikipediaAPIWrapper,
    GoogleTrendsAPIWrapper,
    GoogleScholarAPIWrapper,
    AskNewsAPIWrapper,
    SearxSearchWrapper,
)

from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.utilities.reddit_search import RedditSearchAPIWrapper
from langchain_community.tools.google_scholar import GoogleScholarQueryRun
from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
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
from helpers.config import ToolConfig

tool_conf = ToolConfig()

@tool
def DuckDuckGo(search_query: str):
    """Perform web search using DuckDuckGo."""
    duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)
    return DuckDuckGoSearchRun(
        name="DuckDuckGoSearch",
        api_wrapper=duckduckgo_wrapper,
        description="Use this tool for general-purpose web searches when you need up-to-date or privacy-preserving results.",
    ).run(search_query)

@tool
def Arxiv(search_query: str):
    """Perform academic paper search via Arxiv."""
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=500)
    return ArxivQueryRun(
        name="ArxivSearch",
        api_wrapper=arxiv_wrapper,
        description="Use this tool to search and summarize academic or scientific papers from Arxiv. Ideal for technical or research topics.",
    ).run(search_query)

@tool
def Wikipedia(search_query: str):
    """Perform encyclopedia search via Wikipedia."""
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=500)
    return WikipediaQueryRun(
        name="WikipediaSearch",
        api_wrapper=wiki_wrapper,
        description="Use this tool for general factual or historical information from Wikipedia.",
    ).run(search_query)

@tool
def GoogleSearch(search_query: str):
    """Perform web search using Google."""
    google_wrapper = GoogleSearchAPIWrapper(google_api_key=tool_conf.google_search_api_key, google_cse_id=tool_conf.google_search_cse_id)
    return GoogleSearchRun(
        name="GoogleSearch",
        api_wrapper=google_wrapper,
        description="Use this tool for broad and up-to-date web searches using Google. Ideal for news, websites, or general questions.",
    ).run(search_query)

@tool
def GoogleScholar(search_query: str):
    """Perform academic search via Google Scholar."""
    scholar_wrapper = GoogleScholarAPIWrapper(top_k_results=5, serp_api_key=tool_conf.google_scholar_serp_api_key)
    return GoogleScholarQueryRun(
        name="GoogleScholarSearch",
        api_wrapper=scholar_wrapper,
        description="Use this tool to find peer-reviewed research papers or academic publications from Google Scholar.",
    ).run(search_query)

@tool
def GoogleTrends(search_query: str):
    """Analyze keyword popularity via Google Trends."""
    trends_wrapper = GoogleTrendsAPIWrapper(serp_api_key=tool_conf.google_trend_serp_api_key)
    return GoogleTrendsQueryRun(
        name="GoogleTrends",
        api_wrapper=trends_wrapper,
        description="Use this tool to analyze trending search topics or compare keyword popularity across time or regions.",
    ).run(search_query)

@tool
def AskNews(search_query: str):
    """Search current news headlines and articles."""
    ask_wrapper = AskNewsAPIWrapper(asknews_client_id=tool_conf.asknews_client_id, asknews_client_secret=tool_conf.asknews_client_secret)
    return AskNewsSearch(
        name="AskNews",
        api_wrapper=ask_wrapper,
        description="Use this tool to search for breaking news and recent media coverage on a topic.",
    ).run(search_query)

@tool
def RedditSearch(search_query: str):
    """Search Reddit posts and comments."""
    reddit_wrapper = RedditSearchAPIWrapper(reddit_client_id=tool_conf.reddit_client_id, reddit_client_secret=tool_conf.reddit_client_secret, reddit_user_agent=tool_conf.reddit_user_agent)
    return RedditSearchRun(
        name="RedditSearch",
        api_wrapper=reddit_wrapper,
        description="Use this tool to search Reddit posts and community discussions. Helpful for opinions or social sentiment.",
    ).run(search_query)

@tool
def SearxSearch(search_query: str):
    """Perform privacy-friendly web search using Searx."""
    searxsearch_wrapper = SearxSearchWrapper(searx_host=tool_conf.searx_host)
    return SearxSearchRun(
        name="SearxSearch",
        wrapper=searxsearch_wrapper,
        description="Use this tool for privacy-respecting meta search results across multiple search engines (via Searx).",
    ).run(search_query)

@tool
def OpenWeather(search_query: str):
    """Query weather data via OpenWeatherMap."""
    openweather_wrapper = OpenWeatherMapAPIWrapper(openweathermap_api_key=tool_conf.openweather_api_key)
    return OpenWeatherMapQueryRun(
        name="WeatherQuery",
        api_wrapper=openweather_wrapper,
        description="Use this tool to get current or forecasted weather information for a given location.",
    ).run(search_query)
