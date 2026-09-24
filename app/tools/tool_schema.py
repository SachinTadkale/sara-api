TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the internet for current or recent information. "
                "Use only when the answer depends on up-to-date information "
                "such as news, live events, latest movie release dates, sports, "
                "stock prices, product prices, or recent announcements."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_date_time",
            "description":(
                    "Get the current local date, time, weekday, month, year, and timezone. "
                    "Use when the user asks today's date, current time, day of week, or time."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "Get the current live weather including temperature for a city. "
                "Use when the user asks about current weather, temperature, rain, or climate."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_wikipedia_summary",
            "description": (
                "Retrieve encyclopedic information about people, places, history, science, "
                "movies, books, technologies, organizations and other general knowledge. "
                "Do not use for current news."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The term, concept, person, historical event, or topic to search on Wikipedia."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"lookup_github_repositories",
            "description":"Search public GitHub code repositories for open-source projects, libraries, frameworks, or code repositories.",
            "parameters":{
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search keyword, project name, or technology stack to look up on GitHub (e.g., 'fastapi auth', 'react tailwind dashboard')."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_github_user",
            "description": "Retrieve public profile details, follower counts, and public repository statistics for a specific GitHub user.",
            "parameters": {
            "type": "object",
            "properties": {
                "username": {
                "type": "string",
                "description": "GitHub username"
                }
            },
            "required": ["username"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_github_latest_releases",
            "description": "Fetch the latest published software release, version tag, publication date, and complete markdown changelog/release notes for a specific GitHub repository.",
            "parameters": {
            "type": "object",
            "properties": {
                "owner": {
                "type": "string",
                "description": "The owner or organization name of the repository (e.g., 'kubernetes' or 'octocat')."
                },
                "repo": {
                "type": "string",
                "description": "The specific name of the repository (e.g., 'kubernetes' or 'Hello-World')."
                }
            },
            "required": ["owner", "repo"]
            }
        }
    }
    # {
    #     "type":"function",
    #     "function":{
    #         "name":"currency_converter",
    #         "description":"Convert currency when user asks about to convert money currency",
    #         "parameters":{
    #             ""
    #         }
    #     }
    # }
]