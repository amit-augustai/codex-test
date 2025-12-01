#!/usr/bin/env python3
"""Main entry point for the AI news scraper."""

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

from scraper import scrape_all_sources
from groq_client import GroqClassifier


DATA_DIR = Path(__file__).parent.parent / "data"
NEWS_FILE = DATA_DIR / "news.json"
MAX_ARTICLES = 20  # Target number of articles per day
DAYS_TO_KEEP = 7   # Keep articles for 7 days


def load_existing_news() -> dict:
    """Load existing news data if available."""
    if NEWS_FILE.exists():
        with open(NEWS_FILE, "r") as f:
            return json.load(f)
    return {"lastUpdated": "", "articles": []}


def save_news(data: dict) -> None:
    """Save news data to JSON file."""
    DATA_DIR.mkdir(exist_ok=True)
    with open(NEWS_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def filter_old_articles(articles: list[dict], days: int = DAYS_TO_KEEP) -> list[dict]:
    """Remove articles older than specified days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_str = cutoff.isoformat()

    return [
        article for article in articles
        if article.get("scrapedAt", "") >= cutoff_str
    ]


def deduplicate_articles(new_articles: list[dict], existing_articles: list[dict]) -> list[dict]:
    """Remove duplicate articles based on ID."""
    existing_ids = {article["id"] for article in existing_articles}
    return [article for article in new_articles if article["id"] not in existing_ids]


def main():
    print("=" * 50)
    print("AI News Scraper")
    print(f"Started at: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 50)

    # Load existing news
    existing_data = load_existing_news()
    existing_articles = existing_data.get("articles", [])
    print(f"Loaded {len(existing_articles)} existing articles")

    # Filter out old articles
    existing_articles = filter_old_articles(existing_articles)
    print(f"After filtering old articles: {len(existing_articles)} remaining")

    # Scrape new articles
    print("\nScraping news sources...")
    raw_articles = scrape_all_sources()
    print(f"\nTotal raw articles scraped: {len(raw_articles)}")

    # Deduplicate
    new_articles = deduplicate_articles(raw_articles, existing_articles)
    print(f"New unique articles: {len(new_articles)}")

    if not new_articles:
        print("No new articles to process")
        # Still save to update lastUpdated
        save_news({
            "lastUpdated": datetime.now(timezone.utc).isoformat(),
            "articles": existing_articles,
        })
        return

    # Limit to MAX_ARTICLES new articles
    new_articles = new_articles[:MAX_ARTICLES]
    print(f"Processing {len(new_articles)} new articles with Groq...")

    # Classify articles with Groq
    classifier = GroqClassifier()
    classified_articles = []

    for i, article in enumerate(new_articles):
        print(f"  [{i + 1}/{len(new_articles)}] {article['title'][:50]}...")

        result = classifier.classify_article(
            title=article["title"],
            content=article.get("content", ""),
            default_category=article.get("defaultCategory"),
        )

        classified_article = {
            "id": article["id"],
            "title": article["title"],
            "summary": result["summary"],
            "url": article["url"],
            "source": article["source"],
            "category": result["category"],
            "publishedAt": article["publishedAt"],
            "scrapedAt": article["scrapedAt"],
        }

        if article.get("imageUrl"):
            classified_article["imageUrl"] = article["imageUrl"]

        classified_articles.append(classified_article)
        print(f"    -> Category: {result['category']}")

    # Combine new and existing articles
    all_articles = classified_articles + existing_articles

    # Sort by scraped date (newest first)
    all_articles.sort(key=lambda x: x.get("scrapedAt", ""), reverse=True)

    # Save
    news_data = {
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        "articles": all_articles,
    }
    save_news(news_data)

    print("\n" + "=" * 50)
    print(f"Saved {len(all_articles)} total articles")
    print(f"  - New: {len(classified_articles)}")
    print(f"  - Existing: {len(existing_articles)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
