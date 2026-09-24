import requests 

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "SaraAIAssistant/1.0" # GitHub requires a User-Agent header
}

def lookup_github_user(username:str):

    clean_username = username.strip()
    url = f"https://api.github.com/users/{clean_username}"
    try:
        response = requests.get(url,headers=headers,timeout=10)
        if response.status_code == 404:
            return{"error":f"{clean_username} not found."}
        if response.status_code == 403:
            return{"error":f"Github API rate limit exceeded"}
        response.raise_for_status()

        data = response.json()

        return{
            "username": data.get("login"),
            "name": data.get("name"),
            "bio": data.get("bio"),
            "followers": data.get("followers"),
            "following": data.get("following"),
            "public_repos_count": data.get("public_repos"),
            "profile_url": data.get("html_url"),
        }
    except requests.exceptions.RequestException as e:
        return{"error":f"Github API Error: {str(e)}"}

def lookup_github_repositories(query:str):
    clean_query = query.strip()
    url = f"https://api.github.com/search/repositories?q={clean_query}&per_page=5"

    try:
        response = requests.get(url,headers=headers,timeout=10)

        if response.status_code == 403:
            return {"error": "GitHub API rate limit exceeded. Please try again later."}
        
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])
        if not items:
            return {"message": f"No GitHub repositories found matching '{clean_query}'."}
        results = []
        for item in items:
            results.append({
                "name": item.get("full_name"),
                "description": item.get("description"),
                "stars": item.get("stargazers_count"),
                "language": item.get("language"),
                "url": item.get("html_url")
            })
            
        return {
            "query": clean_query,
            "total_matches": data.get("total_count", 0),
            "top_repositories": results
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to GitHub API: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
    
def get_github_latest_releases(owner:str, repo:str):
    clean_owner = owner.strip()
    clean_repo = repo.strip()
    
    url = f"https://api.github.com/repos/{clean_owner}/{clean_repo}/releases/latest"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "SaraAIAssistant/1.0",
        "X-GitHub-Api-Version": "2026-03-10" # Follows GitHub's calendar versioning rules
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # 404 means either the repo doesn't exist, OR it exists but has 0 releases published yet
        if response.status_code == 404:
            return {"error": f"Latest release not found for '{clean_owner}/{clean_repo}'. (Ensure the repo exists and has a published release)."}
        
        if response.status_code == 403:
            return {"error": "GitHub API rate limit exceeded. Consider adding an authentication token."}
            
        response.raise_for_status()
        data = response.json()
        
        return {
            "tag_name": data.get("tag_name"),           # E.g., "v1.2.3"
            "release_name": data.get("name"),           # E.g., "The Performance Update"
            "published_at": data.get("published_at"),   # E.g., "2026-03-12T14:32:01Z"
            "changelog": data.get("body"),               # Contains the raw markdown release notes
            "html_url": data.get("html_url")            # Direct link to the release on GitHub web
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to GitHub API: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
