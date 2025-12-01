"""News scraper for collecting AI news from various sources."""

import hashlib
import re
from datetime import datetime, timezone
from typing import Optional
import feedparser
import httpx
from bs4 import BeautifulSoup

from sources import Source, RSS_SOURCES, API_SOURCES


def generate_id(url: str) -> str:
    """Generate a unique ID from URL."""
    return hashlib.md5(url.encode()).hexdigest()[:12]


def clean_html(html: str) -> str:
    """Remove HTML tags and clean up text."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text[:1000]  # Limit length


def parse_date(date_str: Optional[str]) -> str:
    """Parse various date formats to ISO format."""
    if not date_str:
        return datetime.now(timezone.utc).isoformat()

    try:
        # feedparser provides a parsed time struct
        import time
        from email.utils import parsedate_to_datetime

        try:
            dt = parsedate_to_datetime(date_str)
            return dt.isoformat()
        except (TypeError, ValueError):
            pass

        # Try common formats
        for fmt in [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]:
            try:
                dt = datetime.strptime(date_str, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.isoformat()
            except ValueError:
                continue

        return datetime.now(timezone.utc).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()


def scrape_rss_source(source: Source) -> list[dict]:
    """Scrape articles from an RSS feed."""
    articles = []

    try:
        feed = feedparser.parse(source.url)

        for entry in feed.entries[:10]:  # Limit to 10 per source
            title = entry.get("title", "").strip()
            link = entry.get("link", "")

            if not title or not link:
                continue

            # Get content
            content = ""
            if hasattr(entry, "content") and entry.content:
                content = entry.content[0].get("value", "")
            elif hasattr(entry, "summary"):
                content = entry.summary
            elif hasattr(entry, "description"):
                content = entry.description

            content = clean_html(content)

            # Get publication date
            pub_date = entry.get("published") or entry.get("updated") or ""

            # Get image if available
            image_url = None
            if hasattr(entry, "media_content") and entry.media_content:
                image_url = entry.media_content[0].get("url")
            elif hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get("url")

            articles.append({
                "id": generate_id(link),
                "title": title,
                "url": link,
                "content": content,
                "source": source.name,
                "publishedAt": parse_date(pub_date),
                "scrapedAt": datetime.now(timezone.utc).isoformat(),
                "imageUrl": image_url,
                "defaultCategory": source.default_category,
            })

    except Exception as e:
        print(f"Error scraping {source.name}: {e}")

    return articles


def scrape_hacker_news(limit: int = 10) -> list[dict]:
    """Scrape AI-related stories from Hacker News."""
    articles = []
    ai_keywords = [
        "ai", "artificial intelligence", "machine learning", "ml", "llm",
        "gpt", "chatgpt", "claude", "openai", "anthropic", "deepmind",
        "neural", "transformer", "diffusion", "generative", "language model"
    ]

    try:
        with httpx.Client(timeout=30) as client:
            # Get top stories
            response = client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            story_ids = response.json()[:100]  # Check top 100 stories

            count = 0
            for story_id in story_ids:
                if count >= limit:
                    break

                story_response = client.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                )
                story = story_response.json()

                if not story or story.get("type") != "story":
                    continue

                title = story.get("title", "").lower()

                # Check if AI-related
                if not any(kw in title for kw in ai_keywords):
                    continue

                url = story.get("url", f"https://news.ycombinator.com/item?id={story_id}")

                articles.append({
                    "id": generate_id(url),
                    "title": story.get("title", ""),
                    "url": url,
                    "content": story.get("text", "") or f"Score: {story.get('score', 0)} points",
                    "source": "Hacker News",
                    "publishedAt": datetime.fromtimestamp(
                        story.get("time", 0), tz=timezone.utc
                    ).isoformat(),
                    "scrapedAt": datetime.now(timezone.utc).isoformat(),
                    "imageUrl": None,
                    "defaultCategory": None,
                })
                count += 1

    except Exception as e:
        print(f"Error scraping Hacker News: {e}")

    return articles


def scrape_all_sources() -> list[dict]:
    """Scrape all configured sources."""
    all_articles = []

    # Scrape RSS sources
    for source in RSS_SOURCES:
        print(f"Scraping {source.name}...")
        articles = scrape_rss_source(source)
        all_articles.extend(articles)
        print(f"  Found {len(articles)} articles")

    # Scrape Hacker News
    print("Scraping Hacker News...")
    hn_articles = scrape_hacker_news(limit=10)
    all_articles.extend(hn_articles)
    print(f"  Found {len(hn_articles)} articles")

    return all_articles
