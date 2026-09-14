"""
Debug script - Google News RSS connection test
Yeh check karega ki request successfully ja rahi hai ya nahi,
aur raw response kaisa aa raha hai.
"""

import requests
import feedparser
from urllib.parse import quote

headers = {"User-Agent": "Mozilla/5.0"}

# Test 1: Bina kisi site filter ke simple search
print("=== TEST 1: Simple search (no site filter) ===")
query1 = "India cricket"
url1 = f"https://news.google.com/rss/search?q={quote(query1)}&hl=en-IN&gl=IN&ceid=IN:en"
print("URL:", url1)

r1 = requests.get(url1, headers=headers, timeout=10)
print("Status code:", r1.status_code)
print("Response length (bytes):", len(r1.content))
print("First 300 chars of response:")
print(r1.text[:300])

feed1 = feedparser.parse(r1.content)
print(f"\nEntries found: {len(feed1.entries)}")
if feed1.entries:
    print("First entry title:", feed1.entries[0].get("title"))
    print("First entry link:", feed1.entries[0].get("link"))

print("\n\n=== TEST 2: With site: filter ===")
query2 = "India cricket site:thehindu.com"
url2 = f"https://news.google.com/rss/search?q={quote(query2)}&hl=en-IN&gl=IN&ceid=IN:en"
print("URL:", url2)

r2 = requests.get(url2, headers=headers, timeout=10)
print("Status code:", r2.status_code)
print("Response length (bytes):", len(r2.content))

feed2 = feedparser.parse(r2.content)
print(f"\nEntries found: {len(feed2.entries)}")
if feed2.entries:
    print("First entry title:", feed2.entries[0].get("title"))
    print("First entry link:", feed2.entries[0].get("link"))