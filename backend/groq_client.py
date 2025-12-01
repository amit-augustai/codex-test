"""Groq LLM client for article categorization and summarization."""

import json
import os
from typing import Optional
from groq import Groq

from sources import Category

CATEGORIES = ['research', 'product', 'company', 'funding', 'policy', 'open-source']

SYSTEM_PROMPT = """You are an AI news categorizer. Given a news article title and content, you must:
1. Categorize it into exactly ONE of these categories:
   - research: Academic papers, scientific breakthroughs, research publications
   - product: New AI tools, features, product launches, updates
   - company: Corporate news, acquisitions, partnerships, leadership changes
   - funding: Investment rounds, valuations, startup funding
   - policy: Government regulations, AI safety discussions, ethics debates
   - open-source: New open-source models, frameworks, libraries, releases

2. Write a concise 1-2 sentence summary of the article.

Respond ONLY with valid JSON in this exact format:
{"category": "<category>", "summary": "<summary>"}
"""


class GroqClassifier:
    def __init__(self, api_key: Optional[str] = None):
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"  # Fast and free tier friendly

    def classify_article(
        self, title: str, content: str, default_category: Optional[Category] = None
    ) -> dict:
        """Classify an article and generate a summary."""
        try:
            user_message = f"Title: {title}\n\nContent: {content[:2000]}"  # Limit content length

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.1,
                max_tokens=256,
            )

            result_text = response.choices[0].message.content.strip()

            # Parse JSON response
            # Handle potential markdown code blocks
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            result = json.loads(result_text)

            # Validate category
            if result.get("category") not in CATEGORIES:
                result["category"] = default_category or "product"

            return {
                "category": result.get("category", default_category or "product"),
                "summary": result.get("summary", content[:200] if content else title),
            }

        except Exception as e:
            print(f"Error classifying article: {e}")
            # Fallback to default category and truncated content as summary
            return {
                "category": default_category or "product",
                "summary": content[:200] if content else title,
            }
