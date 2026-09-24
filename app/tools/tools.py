from app.tools.web_search import web_search
from app.tools.get_date_time import get_date_time
from app.tools.get_weather import get_weather
from app.tools.wikipedia import get_wikipedia_summary
from app.tools.github import lookup_github_repositories,lookup_github_user,get_github_latest_releases

TOOL_FUNCTIONS = {
    "web_search": web_search,
    "get_date_time": get_date_time,
    "get_weather": get_weather,
    "get_wikipedia_summary": get_wikipedia_summary,
    "lookup_github_repositories": lookup_github_repositories,
    "lookup_github_user": lookup_github_user,
    "get_github_latest_releases": get_github_latest_releases,
}