from ddgs import DDGS
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

def _parse_timelimit(recency_days) -> str | None:
    """Map recency_days or string timelimit to DuckDuckGo valid values: 'd', 'w', 'm', 'y', or None."""
    if recency_days is None:
        return None

    # If already a valid code string
    if isinstance(recency_days, str):
        val = recency_days.strip().lower()
        if val in {"d", "w", "m", "y"}:
            return val
        if val in {"day", "today", "1d"}:
            return "d"
        if val in {"week", "7d", "1w"}:
            return "w"
        if val in {"month", "30d", "1m"}:
            return "m"
        if val in {"year", "365d", "1y"}:
            return "y"
        try:
            recency_days = int(val)
        except ValueError:
            return None

    try:
        days = int(recency_days)
        if days <= 0:
            return None
        if days <= 1:
            return "d"
        if days <= 7:
            return "w"
        if days <= 31:
            return "m"
        if days <= 365:
            return "y"
        return None
    except (ValueError, TypeError):
        return None

# Cache recent queries to avoid repeated network calls
@lru_cache(maxsize=64)
def _search_ddg(query: str, max_results: int, timelimit: str | None, timeout: int) -> list:
    """Internal helper that performs the DDG request with safe arguments."""
    try:
        with DDGS(timeout=timeout) as ddgs:
            kwargs = {"max_results": max_results}
            if timelimit:
                kwargs["timelimit"] = timelimit
            results = ddgs.text(query, **kwargs)
            return list(results)[:max_results] if results else []
    except Exception as exc:
        logger.warning(f"Web search failed for query [{query}]: {exc}")
        return []

def web_search(query: str, top_n: int = 5, recency_days=None, timelimit=None, timeout: int = 5, **kwargs) -> list:
    """Perform a DuckDuckGo text search with sane defaults.

    Args:
        query: The search string.
        top_n: Maximum number of results to return (default 5, capped at 5).
        recency_days: Optional integer days to filter (e.g. 1, 7, 30, 365).
        timelimit: Optional string ('d', 'w', 'm', 'y').
        timeout: Maximum seconds to wait for the HTTP request (default 5).
        **kwargs: Ignored – kept for backward compatibility.

    Returns:
        A list of result dictionaries. Empty list on error.
    """
    try:
        max_res = int(top_n)
    except (ValueError, TypeError):
        max_res = 5
    max_res = max(1, min(max_res, 5))

    parsed_timelimit = _parse_timelimit(timelimit or recency_days)
    return _search_ddg(query, max_res, parsed_timelimit, timeout)