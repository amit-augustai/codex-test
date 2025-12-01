"""News source configurations for AI news scraping."""

from dataclasses import dataclass
from typing import Literal, Optional

Category = Literal['research', 'product', 'company', 'funding', 'policy', 'open-source']

@dataclass
class Source:
    name: str
    url: str
    source_type: Literal['rss', 'api']
    default_category: Optional[Category] = None


# RSS Feed Sources
RSS_SOURCES = [
    Source(
        name="MIT Technology Review - AI",
        url="https://www.technologyreview.com/topic/artificial-intelligence/feed",
        source_type="rss",
    ),
    Source(
        name="Google AI Blog",
        url="https://blog.google/technology/ai/rss/",
        source_type="rss",
        default_category="research",
    ),
    Source(
        name="OpenAI Blog",
        url="https://openai.com/blog/rss.xml",
        source_type="rss",
        default_category="research",
    ),
    Source(
        name="TechCrunch - AI",
        url="https://techcrunch.com/category/artificial-intelligence/feed/",
        source_type="rss",
    ),
    Source(
        name="VentureBeat - AI",
        url="https://venturebeat.com/category/ai/feed/",
        source_type="rss",
    ),
    Source(
        name="arXiv - AI",
        url="https://rss.arxiv.org/rss/cs.AI",
        source_type="rss",
        default_category="research",
    ),
    Source(
        name="arXiv - Machine Learning",
        url="https://rss.arxiv.org/rss/cs.LG",
        source_type="rss",
        default_category="research",
    ),
    Source(
        name="The Verge - AI",
        url="https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        source_type="rss",
    ),
    Source(
        name="Wired - AI",
        url="https://www.wired.com/feed/tag/ai/latest/rss",
        source_type="rss",
    ),
]

# API Sources
API_SOURCES = [
    Source(
        name="Hacker News",
        url="https://hacker-news.firebaseio.com/v0",
        source_type="api",
    ),
]

ALL_SOURCES = RSS_SOURCES + API_SOURCES
