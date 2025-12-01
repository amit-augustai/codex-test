export type Category =
  | 'research'
  | 'product'
  | 'company'
  | 'funding'
  | 'policy'
  | 'open-source';

export interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  url: string;
  source: string;
  category: Category;
  publishedAt: string;
  scrapedAt: string;
  imageUrl?: string;
}

export interface NewsData {
  lastUpdated: string;
  articles: NewsArticle[];
}

export interface RawArticle {
  title: string;
  link: string;
  content?: string;
  contentSnippet?: string;
  pubDate?: string;
  source: string;
}

export interface SourceConfig {
  name: string;
  type: 'rss' | 'api';
  url: string;
  category?: Category;
}

export interface GroqClassification {
  category: Category;
  summary: string;
}
