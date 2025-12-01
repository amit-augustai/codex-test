'use client';

interface HeaderProps {
  lastUpdated: string;
}

export default function Header({ lastUpdated }: HeaderProps) {
  const formatDate = (dateStr: string) => {
    if (!dateStr) return 'Never';
    try {
      const date = new Date(dateStr);
      return date.toLocaleString();
    } catch {
      return 'Unknown';
    }
  };

  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">AI News Dashboard</h1>
            <p className="text-blue-100 mt-1">
              Daily curated AI news from around the world
            </p>
          </div>
          <div className="text-sm text-blue-100">
            <span className="opacity-75">Last updated:</span>{' '}
            <span className="font-medium">{formatDate(lastUpdated)}</span>
          </div>
        </div>
      </div>
    </header>
  );
}
