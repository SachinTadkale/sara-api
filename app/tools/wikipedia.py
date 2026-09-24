import requests

HEADERS = {
    "User-Agent":"SaraAIAssistant-1.0"
}

def get_wikipedia_summary(query:str):
    query_clean = query.strip()

    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action":"query",
        "list":"search",
        "sresearch":query_clean,
        "format":"json",
        "utf8":1
    }

    try:
        search_res = requests.get(search_url,params=search_params,headers=HEADERS,timeout=10)
        search_res.raise_for_status()
        search_data = search_res.json()

        search_results = search_data.get("query",{}).get("search",[])
        if not search_results:
            return {"error": f"No Wikipedia pages found matching '{query_clean}'."}
        
        best_match_title = search_results[0]["title"]
        formatted_title = best_match_title.replace(" ","_")
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_title}"

        summary_res = requests.get(summary_url, headers=HEADERS, timeout=10)
        summary_res.raise_for_status()
        summary_data = summary_res.json()
        return {
            "title": summary_data.get("title"),
            "summary": summary_data.get("extract"),
            "url": summary_data.get("content_urls", {}).get("desktop", {}).get("page")
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to Wikipedia API: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}