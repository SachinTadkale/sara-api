import requests

def get_raw_hn_news():
    top_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:8]

    stories = []
    for item_id in top_ids:
        story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json").json()
        if story and story.get("type") == "story":
            stories.append({
                "title": story.get("title"),
                "score": story.get("score"),
                "url": story.get("url",f"https://news.ycombinator.com/item?id={item_id}")
            })
    return stories