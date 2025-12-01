import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';
import { validateApiKey, unauthorizedResponse } from '@/lib/auth';
import type { NewsData, Category } from '@/types/news';

const DATA_FILE = path.join(process.cwd(), 'data', 'news.json');

async function loadNewsData(): Promise<NewsData> {
  try {
    const data = await fs.readFile(DATA_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    return { lastUpdated: '', articles: [] };
  }
}

export async function GET(request: NextRequest) {
  // Validate API key
  if (!validateApiKey(request)) {
    return unauthorizedResponse();
  }

  try {
    const newsData = await loadNewsData();

    // Get query params for filtering
    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category') as Category | null;
    const source = searchParams.get('source');
    const limit = parseInt(searchParams.get('limit') || '50', 10);
    const offset = parseInt(searchParams.get('offset') || '0', 10);

    let articles = newsData.articles;

    // Filter by category
    if (category) {
      articles = articles.filter((a) => a.category === category);
    }

    // Filter by source
    if (source) {
      articles = articles.filter((a) =>
        a.source.toLowerCase().includes(source.toLowerCase())
      );
    }

    // Apply pagination
    const total = articles.length;
    articles = articles.slice(offset, offset + limit);

    return NextResponse.json({
      lastUpdated: newsData.lastUpdated,
      total,
      offset,
      limit,
      articles,
    });
  } catch (error) {
    console.error('Error loading news:', error);
    return NextResponse.json(
      { error: 'Failed to load news data' },
      { status: 500 }
    );
  }
}
