import json
from app.client.openai import client
from app.tools.hacker_news import get_raw_hn_news
from app.config.settings import CHAT_MODEL
from fastapi import HTTPException

def get_hacker_news():
    raw_news = get_raw_hn_news()
    prompt = f"""
    You are a JSON generator. Use this raw tech news data:
    {json.dumps(raw_news)}

    RULES:
    1. Output ONLY a raw JSON object. No markdown, no wrappers, no extra text.
    2. Translate all content into very simple, plain English. Avoid all technical jargon and big, complicated words (e.g., use "making tech smaller" instead of "miniaturization").
    3. Process and include exactly 4 stories in the "news" list based on the highest scores and best topics.
    4. For each news item, include a simple one-word category (e.g., "AI", "Security", "System", "Software").

    JSON Structure:
    {{
        "summary": "Good Morning, Sachin. Today's discussions are dominated by [Summarize 2-3 main trends in 1 short, simple sentence].",
        "news": [
            {{
                "title": "[Simple rewritten title without hard words]",
                "category": "[One-word category]",
                "score": 450,
                "teaser": "[1-sentence explanation of what this means in simple words]",
                "url": "[Original story URL]"
            }},
            {{
                "title": "[Simple rewritten title without hard words]",
                "category": "[One-word category]",
                "score": 120,
                "teaser": "[1-sentence explanation of what this means in simple words]",
                "url": "[Original story URL]"
            }}
            // ... continue this exact structure to output exactly 4 items total
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model= CHAT_MODEL,
            response_format= {"type":"json_object"},
            messages= [{"role":"user","content":prompt}]
        )
        ai_payload = json.loads(response.choices[0].message.content)
        return ai_payload    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM data extraction failed: {str(e)}")