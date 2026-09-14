"""
Google News RSS verification using trusted publishers.
No web scraping is used.
"""

from typing import Dict, List
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

import requests

TRUSTED_SOURCES = {
    "The Hindu": "thehindu.com",
    "Hindustan Times": "hindustantimes.com",
    "Amar Ujala": "amarujala.com",
}


def _extract_keywords(text: str, max_words: int = 8) -> str:
    words = [word.strip() for word in text.split() if word.strip()]
    return " ".join(words[:max_words])


def _fetch_google_news_rss(query: str, limit: int = 5) -> List[Dict[str, str]]:
    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = root.findall("./channel/item")

    results = []
    for item in items[:limit]:
        title = item.findtext("title", default="")
        link = item.findtext("link", default="")
        pub_date = item.findtext("pubDate", default="")
        results.append({"title": title, "link": link, "published": pub_date})
    return results


def verify_with_trusted_sources(news_text: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Search Google News RSS for each trusted source.
    Returns headlines grouped by source.
    """
    keywords = _extract_keywords(news_text)
    results: Dict[str, List[Dict[str, str]]] = {}

    if not keywords:
        return results

    for source_name, domain in TRUSTED_SOURCES.items():
        query = f"{keywords} site:{domain}"
        try:
            results[source_name] = _fetch_google_news_rss(query)
        except requests.RequestException:
            results[source_name] = []
    return results
