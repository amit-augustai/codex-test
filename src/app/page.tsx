import { promises as fs } from 'fs';
import path from 'path';
import Dashboard from '@/components/Dashboard';
import type { NewsData } from '@/types/news';

async function getNewsData(): Promise<NewsData> {
  try {
    const dataPath = path.join(process.cwd(), 'data', 'news.json');
    const data = await fs.readFile(dataPath, 'utf-8');
    return JSON.parse(data);
  } catch {
    return { lastUpdated: '', articles: [] };
  }
}

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function Home() {
  const newsData = await getNewsData();

  return (
    <Dashboard
      articles={newsData.articles}
      lastUpdated={newsData.lastUpdated}
    />
  );
}
