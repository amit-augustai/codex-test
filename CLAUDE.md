# CLAUDE.md - AI Assistant Guidelines

This file provides context and guidelines for AI assistants working with this codebase.

## Repository Overview

**Repository Name:** codex-test (AI News Dashboard)
**Status:** Active Development

A Vercel-compatible Next.js application that scrapes AI-related news daily and displays them in a categorized dashboard.

## Project Structure

```
codex-test/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── api/news/route.ts   # Protected news API
│   │   ├── page.tsx            # Dashboard page
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Tailwind styles
│   ├── components/
│   │   ├── Dashboard.tsx       # Main dashboard component
│   │   ├── Header.tsx          # Page header
│   │   ├── CategoryFilter.tsx  # Category filter buttons
│   │   └── NewsCard.tsx        # Article card component
│   ├── lib/
│   │   └── auth.ts             # API authentication
│   └── types/
│       └── news.ts             # TypeScript interfaces
├── backend/                    # Python scraper
│   ├── main.py                 # Entry point
│   ├── scraper.py              # RSS/API scraping
│   ├── groq_client.py          # Groq LLM integration
│   ├── sources.py              # News source configs
│   └── requirements.txt        # Python dependencies
├── data/
│   └── news.json               # Scraped articles (auto-updated)
├── .github/workflows/
│   └── scrape.yml              # Daily GitHub Action
├── .env.example                # Environment template
├── package.json                # Node dependencies
└── CLAUDE.md                   # This file
```

## Key Commands

```bash
# Install dependencies
npm install
pip install -r backend/requirements.txt

# Run Next.js dev server
npm run dev

# Run Python scraper
GROQ_API_KEY=your_key python backend/main.py

# Build for production
npm run build

# Lint
npm run lint
```

## Architecture Notes

### Frontend (Next.js)
- Uses App Router with server components
- Dashboard reads directly from `data/news.json`
- Protected API route at `/api/news` for external access
- Tailwind CSS for styling with dark mode support

### Backend (Python)
- Scrapes RSS feeds and APIs for AI news
- Uses Groq LLM (llama-3.1-8b-instant) for categorization
- Runs daily via GitHub Actions
- Commits updated `news.json` to repo

### Categories
- research, product, company, funding, policy, open-source

## Environment Variables

| Variable | Description | Used By |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM | Python scraper |
| `API_SECRET_KEY` | API auth key | Next.js API routes |

## AI Assistant Guidelines

When working with this codebase:

1. **Read before modifying** - Always read existing code before changes
2. **Follow existing patterns** - Match TypeScript/Python conventions in use
3. **Minimize changes** - Only change what's necessary
4. **Test locally** - Run `npm run dev` and verify changes work
5. **Update data types** - Keep `src/types/news.ts` in sync with Python

### What to Avoid

- Don't modify `data/news.json` directly (auto-generated)
- Don't add new dependencies without justification
- Don't change the scraper schedule without discussion
- Don't expose API keys or secrets

## Dependencies

### Node.js (package.json)
- next, react, react-dom - Core framework
- tailwindcss - Styling

### Python (requirements.txt)
- feedparser - RSS parsing
- httpx - HTTP client
- groq - Groq LLM SDK
- beautifulsoup4 - HTML parsing
- python-dotenv - Environment variables

---

*Last updated: 2025-12-01*
