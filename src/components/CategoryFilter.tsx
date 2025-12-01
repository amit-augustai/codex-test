'use client';

import type { Category } from '@/types/news';

interface CategoryFilterProps {
  selectedCategory: Category | 'all';
  onCategoryChange: (category: Category | 'all') => void;
  categoryCounts: Record<string, number>;
}

const CATEGORIES: { value: Category | 'all'; label: string; color: string }[] = [
  { value: 'all', label: 'All', color: 'bg-gray-500' },
  { value: 'research', label: 'Research', color: 'bg-blue-500' },
  { value: 'product', label: 'Product', color: 'bg-green-500' },
  { value: 'company', label: 'Company', color: 'bg-purple-500' },
  { value: 'funding', label: 'Funding', color: 'bg-yellow-500' },
  { value: 'policy', label: 'Policy', color: 'bg-red-500' },
  { value: 'open-source', label: 'Open Source', color: 'bg-orange-500' },
];

export default function CategoryFilter({
  selectedCategory,
  onCategoryChange,
  categoryCounts,
}: CategoryFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {CATEGORIES.map(({ value, label, color }) => {
        const count = value === 'all'
          ? Object.values(categoryCounts).reduce((a, b) => a + b, 0)
          : categoryCounts[value] || 0;
        const isSelected = selectedCategory === value;

        return (
          <button
            key={value}
            onClick={() => onCategoryChange(value)}
            className={`
              px-4 py-2 rounded-full text-sm font-medium transition-all
              ${isSelected
                ? `${color} text-white shadow-md scale-105`
                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
              }
            `}
          >
            {label}
            <span className={`ml-2 ${isSelected ? 'opacity-80' : 'opacity-60'}`}>
              ({count})
            </span>
          </button>
        );
      })}
    </div>
  );
}

export function getCategoryColor(category: Category): string {
  const colors: Record<Category, string> = {
    research: 'bg-blue-500',
    product: 'bg-green-500',
    company: 'bg-purple-500',
    funding: 'bg-yellow-500',
    policy: 'bg-red-500',
    'open-source': 'bg-orange-500',
  };
  return colors[category] || 'bg-gray-500';
}
