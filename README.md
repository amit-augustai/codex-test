# AI News Dashboard

A Vercel-compatible Next.js application that scrapes AI-related news from various sources and displays them in a categorized dashboard. News is fetched daily via GitHub Actions and categorized using Groq LLM.

## Features

- Daily automated news scraping via GitHub Actions
- AI-powered categorization and summarization using Groq
- Dashboard with filtering and search
- Dark mode support
- Protected API endpoint

## Categories

- **Research** - Academic papers, scientific breakthroughs
- **Product** - New AI tools, features, product launches
- **Company** - Corporate news, acquisitions, partnerships
- **Funding** - Investment rounds, valuations
- **Policy** - Government regulations, AI safety discussions
- **Open Source** - New models, frameworks, releases

## News Sources

- MIT Technology Review
- Google AI Blog
- OpenAI Blog
- TechCrunch AI
- VentureBeat AI
- arXiv (cs.AI, cs.LG)
- The Verge AI
- Wired AI
- Hacker News (AI-related)

## Project Structure

```
├── src/
│   ├── app/              # Next.js App Router
│   │   ├── api/news/     # Protected news API
│   │   └── page.tsx      # Dashboard page
│   ├── components/       # React components
│   ├── lib/              # Utilities (auth, etc.)
│   └── types/            # TypeScript types
├── backend/              # Python scraper
│   ├── main.py           # Entry point
│   ├── scraper.py        # Scraping logic
│   ├── groq_client.py    # Groq LLM integration
│   ├── sources.py        # News source configs
│   └── requirements.txt  # Python dependencies
├── data/
│   └── news.json         # Scraped news data
└── .github/workflows/
    └── scrape.yml        # Daily scraping workflow
```

## Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- Groq API key (free at https://console.groq.com)

### Local Development

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd codex-test
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Create `.env.local` file:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API keys
   ```

5. Run the scraper (optional, to populate data):
   ```bash
   GROQ_API_KEY=your_key python backend/main.py
   ```

6. Start the development server:
   ```bash
   npm run dev
   ```

7. Open http://localhost:3000

### GitHub Actions Setup

1. Go to your repo Settings > Secrets and variables > Actions
2. Add these secrets:
   - `GROQ_API_KEY` - Your Groq API key

The scraper runs daily at 8:00 AM UTC. You can also trigger it manually from the Actions tab.

### Vercel Deployment

1. Connect your repo to Vercel
2. Add environment variables:
   - `API_SECRET_KEY` - Your API secret for protected endpoints
3. Deploy

## API Endpoints

### GET /api/news

Protected endpoint to fetch news articles.

**Headers:**
- `x-api-key`: Your API secret key

**Query Parameters:**
- `category` - Filter by category
- `source` - Filter by source name
- `limit` - Number of articles (default: 50)
- `offset` - Pagination offset (default: 0)

**Example:**
```bash
curl -H "x-api-key: your_key" "https://your-app.vercel.app/api/news?category=research&limit=10"
```

## Development

```bash
# Run Next.js dev server
npm run dev

# Run Python scraper locally
GROQ_API_KEY=your_key python backend/main.py

# Build for production
npm run build

# Lint
npm run lint
```

## License

MIT
