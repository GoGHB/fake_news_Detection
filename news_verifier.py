"""
Real-Time News Verification Module (Google News RSS version - NO API KEY NEEDED)
-----------------------------------------------------------------------------------
Google News ki free RSS feed use karta hai, aur teeno trusted Indian
newspapers ko ALAG-ALAG search karta hai (ek combined OR query se
Google News RSS reliably kaam nahi karta - isliye yeh fix kiya):
    - The Hindu (thehindu.com)
    - Hindustan Times (hindustantimes.com)
    - Amar Ujala (amarujala.com)

Setup:
    python -m pip install feedparser requests --break-system-packages
"""

import requests
import feedparser
from urllib.parse import quote
from datetime import datetime

TRUSTED_DOMAINS = ["thehindu.com", "hindustantimes.com", "amarujala.com"]


def search_single_domain(claim: str, domain: str, lang: str = "en-IN", country: str = "IN"):
    """
    Ek specific domain (jaise thehindu.com) ke liye Google News RSS search karta hai.
    """
    query = f"{claim} site:{domain}"
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl={lang}&gl={country}&ceid={country}:{lang.split('-')[0]}"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    feed = feedparser.parse(response.content)

    results = []
    for entry in feed.entries[:5]:   # top 5 hi rakho har domain se, zyada ki zaroorat nahi
        link = entry.get("link", "")
        title = entry.get("title", "")
        published = entry.get("published", "")

        # Note: Google News links redirect URLs hote hain (news.google.com/rss/articles/...),
        # asli domain link mein nahi hota — isliye yahan koi domain-check nahi lagana.
        # site: filter query mein hi lagaya gaya hai, wahi kaafi hai.
        results.append({
            "title": title,
            "link": link,
            "source": domain,
            "published": published
        })
    return results


def search_related_news(claim: str):
    """
    Teeno trusted domains ko alag-alag search karke results merge karta hai.
    """
    all_articles = []
    for domain in TRUSTED_DOMAINS:
        try:
            articles = search_single_domain(claim, domain)
            all_articles.extend(articles)
        except Exception:
            # ek domain fail ho jaye to baaki domains try karte rehna
            continue
    return all_articles


def verify_claim(claim: str) -> dict:
    """
    Main function: claim ko The Hindu / Hindustan Times / Amar Ujala se verify karta hai.
    """
    articles = search_related_news(claim)
    match_count = len(articles)

    if match_count >= 2:
        verdict = "Likely Real — multiple trusted Indian newspapers cover this story"
    elif match_count == 1:
        verdict = "Possibly Real — one trusted source found, verify further"
    else:
        verdict = "No matching coverage found in The Hindu / Hindustan Times / Amar Ujala"

    return {
        "total_articles_found": match_count,
        "trusted_source_matches": match_count,
        "trusted_articles": articles,
        "verdict": verdict,
        "checked_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    test_claim = "India cricket match win"
    print(f"Checking claim: {test_claim}\n")

    result = verify_claim(test_claim)

    print("Verdict:", result["verdict"])
    print("Total articles found:", result["total_articles_found"])
    print("\nMatching articles:")
    for art in result["trusted_articles"][:10]:
        print(f"  - [{art['source']}] {art['title']}")
        print(f"    {art['link']}")