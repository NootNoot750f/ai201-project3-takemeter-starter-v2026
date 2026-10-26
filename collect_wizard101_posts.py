#!/usr/bin/env python3
"""
Collect public r/Wizard101 posts from Reddit's RSS feed into labels.csv.

This script only collects text and source links. It deliberately leaves labels
blank; label 20 posts yourself first and mark those rows "cold".
"""
import csv
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

OUTFILE = Path("labels.csv")
TARGET = 200
USER_AGENT = "AI201 student dataset project"
ATOM = "{http://www.w3.org/2005/Atom}"
REDDIT = "https://www.reddit.com"

def fetch_feed(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        return ET.fromstring(response.read())

def get_text(entry, tag):
    node = entry.find(ATOM + tag)
    return "" if node is None or node.text is None else node.text.strip()

def main():
    rows = []
    seen = set()
    # RSS search supports pagination via after in many Reddit feed contexts.
    # Start with the newest feed, then use the last entry's permalink as "after".
    url = f"{REDDIT}/r/Wizard101/new/.rss?limit=100"
    pages = 0

    while len(rows) < TARGET and pages < 10:
        pages += 1
        try:
            root = fetch_feed(url)
        except urllib.error.HTTPError as exc:
            print(f"Reddit RSS returned HTTP {exc.code}; stopping.")
            break
        except Exception as exc:
            print(f"Could not read Reddit RSS: {exc}")
            break

        entries = root.findall(ATOM + "entry")
        if not entries:
            print("The feed returned no entries.")
            break

        for entry in entries:
            title = get_text(entry, "title")
            content = get_text(entry, "content")
            link_node = entry.find(ATOM + "link")
            link = link_node.attrib.get("href", "") if link_node is not None else ""
            # Use the link as a stable duplicate key.
            if not link or link in seen:
                continue
            seen.add(link)

            # RSS content is HTML; preserve its readable text without truncating.
            import html
            import re
            content = html.unescape(re.sub(r"<[^>]+>", " ", content))
            content = re.sub(r"\s+", " ", content).strip()
            title = html.unescape(title).strip()
            full_text = title if not content or content == title else f"{title}\n\n{content}"
            if not full_text.strip():
                continue

            rows.append({
                "text": full_text,
                "label": "",
                "note": f"source: {link}"
            })
            if len(rows) >= TARGET:
                break

        # RSS endpoints don't reliably support paging. Stop rather than loop on duplicates.
        if len(rows) < TARGET:
            print(f"Feed page {pages}: collected {len(rows)} unique posts.")
            print("Reddit's RSS endpoint may only expose the newest page; checking if it supports an 'after' cursor.")
            last_link = entries[-1].find(ATOM + "link")
            if last_link is None:
                break
            after = last_link.attrib.get("href", "")
            if not after:
                break
            # Try a time-bounded subreddit RSS search before giving up.
            # Reddit RSS search uses the query parameter and may return a different set.
            url = f"{REDDIT}/r/Wizard101/search/.rss?" + urllib.parse.urlencode({
                "q": "wizard101",
                "restrict_sr": "on",
                "sort": "new",
                "t": "all",
                "limit": 100,
            })
            time.sleep(1)
            # One fallback search page is enough; if it repeats, deduplication ends it.
            if pages >= 2:
                break

    with OUTFILE.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label", "note"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} unique posts to {OUTFILE.resolve()}")
    if len(rows) < TARGET:
        print("This feed did not provide 200 unique posts. The CSV is a partial collection, not a 200-post dataset.")
        print("Do not submit it as 200; we can combine it with more public RSS/search results.")
    print("Labels are blank by design. Label 20 posts independently and set their note to 'cold'.")

if __name__ == "__main__":
    main()
