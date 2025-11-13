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

from databases.crud import get_tool_by_name
from databases.database import SessionLocal

async def get_tool_conf(tool_name: str):
    """Fetch tool credentials from the database."""
    async with SessionLocal() as session:
        return await get_tool_by_name(session, tool_name)
    
@tool
async def DuckDuckGo(search_query: str):
    """Perform web search using DuckDuckGo."""
    db_tool = await get_tool_conf("duckduckgo")
    duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)
    return DuckDuckGoSearchRun(
        name="DuckDuckGoSearch",
        api_wrapper=duckduckgo_wrapper,
        description="Use this tool for general-purpose web searches when you need up-to-date or privacy-preserving results.",
    ).run(search_query)

@tool
async def Arxiv(search_query: str):
    """Perform academic paper search via Arxiv."""
    db_tool = await get_tool_conf("arxiv")
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=500)
    return ArxivQueryRun(
        name="ArxivSearch",
        api_wrapper=arxiv_wrapper,
        description="Use this tool to search and summarize academic or scientific papers from Arxiv. Ideal for technical or research topics.",
    ).run(search_query)

@tool
async def Wikipedia(search_query: str):
    """Perform encyclopedia search via Wikipedia."""
    db_tool = await get_tool_conf("wikipedia")
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=500)
    return WikipediaQueryRun(
        name="WikipediaSearch",
        api_wrapper=wiki_wrapper,
        description="Use this tool for general factual or historical information from Wikipedia.",
    ).run(search_query)

@tool
async def GoogleSearch(search_query: str):
    """Perform web search using Google."""
    db_tool = await get_tool_conf("google_search")
    google_wrapper = GoogleSearchAPIWrapper(
        google_api_key=db_tool.api_key,
        google_cse_id=db_tool.cse_id,
    )
    return GoogleSearchRun(
        name="GoogleSearch",
        api_wrapper=google_wrapper,
        description="Use this tool for broad and up-to-date web searches using Google.",
    ).run(search_query)

@tool
async def GoogleScholar(search_query: str):
    """Perform academic search via Google Scholar."""
    db_tool = await get_tool_conf("google_scholar")
    scholar_wrapper = GoogleScholarAPIWrapper(
        top_k_results=5,
        serp_api_key=db_tool.api_key,
    )
    return GoogleScholarQueryRun(
        name="GoogleScholarSearch",
        api_wrapper=scholar_wrapper,
        description="Use this tool to find peer-reviewed research papers from Google Scholar.",
    ).run(search_query)

@tool
async def GoogleTrends(search_query: str):
    """Analyze keyword popularity via Google Trends."""
    db_tool = await get_tool_conf("google_trends")
    trends_wrapper = GoogleTrendsAPIWrapper(serp_api_key=db_tool.api_key)
    return GoogleTrendsQueryRun(
        name="GoogleTrends",
        api_wrapper=trends_wrapper,
        description="Use this tool to analyze trending search topics over time or regions.",
    ).run(search_query)

@tool
async def AskNews(search_query: str):
    """Search current news headlines and articles."""
    db_tool = await get_tool_conf("asknews")
    ask_wrapper = AskNewsAPIWrapper(
        asknews_client_id=db_tool.client_id,
        asknews_client_secret=db_tool.client_secret,
    )
    return AskNewsSearch(
        name="AskNews",
        api_wrapper=ask_wrapper,
        description="Use this tool to search for breaking news and recent media coverage.",
    ).run(search_query)

@tool
async def RedditSearch(search_query: str):
    """Search Reddit posts and comments."""
    db_tool = await get_tool_conf("reddit")
    reddit_wrapper = RedditSearchAPIWrapper(
        reddit_client_id=db_tool.client_id,
        reddit_client_secret=db_tool.client_secret,
        reddit_user_agent=db_tool.user_agent,
    )
    return RedditSearchRun(
        name="RedditSearch",
        api_wrapper=reddit_wrapper,
        description="Use this tool to search Reddit posts and community discussions.",
    ).run(search_query)

@tool
async def SearxSearch(search_query: str):
    """Perform privacy-friendly web search using Searx."""
    db_tool = await get_tool_conf("searx")
    searx_wrapper = SearxSearchWrapper(searx_host=db_tool.host)
    return SearxSearchRun(
        name="SearxSearch",
        wrapper=searx_wrapper,
        description="Use this tool for privacy-respecting meta search results across multiple engines.",
    ).run(search_query)

@tool
async def OpenWeather(search_query: str):
    """Query weather data via OpenWeatherMap."""
    db_tool = await get_tool_conf("openweather")
    openweather_wrapper = OpenWeatherMapAPIWrapper(openweathermap_api_key=db_tool.api_key)
    return OpenWeatherMapQueryRun(
        name="WeatherQuery",
        api_wrapper=openweather_wrapper,
        description="Use this tool to get current or forecasted weather information for a given location.",
    ).run(search_query)
