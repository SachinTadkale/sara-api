from ddgs import DDGS
def web_search(query: str):
    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            max_results = 5
        )

        return list(results)