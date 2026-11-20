"""Trending-topic scraper.

Uses the public, keyless Hacker News API as a stand-in trend source: no login,
no API key, no rate-limit headaches. If the network call fails (offline,
blocked, rate-limited) it retries once, then falls back to a small fixed
topic list so the rest of the pipeline still runs.
"""
import json
import time
import urllib.request

HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"

FALLBACK_TOPICS = [
    "batch cooking on a budget",
    "fixing a leaky faucet yourself",
    "a morning routine that actually sticks",
    "pricing your first freelance quote",
    "organizing a small closet",
]


def _fetch_json(url, timeout=5):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())


def fetch_trending_topics(limit=5, retries=1):
    """Return up to `limit` current Hacker News front-page titles.

    Falls back to FALLBACK_TOPICS on any network failure, after one retry.
    """
    for attempt in range(retries + 1):
        try:
            ids = _fetch_json(HN_TOP_STORIES)[:limit]
            titles = []
            for item_id in ids:
                item = _fetch_json(HN_ITEM.format(item_id))
                title = (item or {}).get("title")
                if title:
                    titles.append(title)
            if titles:
                return titles
            break
        except Exception:
            if attempt < retries:
                time.sleep(1)
                continue
            break
    return FALLBACK_TOPICS[:limit]
