import React, { useRef } from 'react';
import { Search, X, ArrowRight } from 'lucide-react';

export default function SearchBar({
  query,
  setQuery,
  onSearch,
  isLoading,
  onSelectExample,
}) {
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const handleClear = () => {
    setQuery('');
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const exampleQueries = [
    'Find my notes about machine learning.',
    'Show me screenshots related to Python.',
    'Find documents about database management.',
  ];

  return (
    <div className="w-full max-w-3xl">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-center">
          <Search className="absolute left-4 w-5 h-5 text-slate-400 pointer-events-none" />
          
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Find something you remember..."
            className="w-full pl-11 pr-24 py-3.5 text-base rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 shadow-xs focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 dark:focus:border-emerald-500 transition-all"
            disabled={isLoading}
          />

          <div className="absolute right-2 flex items-center gap-1.5">
            {query && (
              <button
                type="button"
                onClick={handleClear}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                title="Clear input"
                aria-label="Clear input"
              >
                <X className="w-4 h-4" />
              </button>
            )}

            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="flex items-center gap-1.5 px-3.5 py-2 text-sm font-medium rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-xs"
            >
              <span>Search</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </form>

      {/* Suggested queries */}
      {exampleQueries && exampleQueries.length > 0 && (
        <div className="mt-3 flex flex-wrap items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
          <span className="font-medium text-slate-400 dark:text-slate-500">
            Try:
          </span>
          {exampleQueries.map((example, i) => (
            <button
              key={i}
              type="button"
              onClick={() => onSelectExample && onSelectExample(example)}
              className="px-2.5 py-1 rounded-md bg-white border border-slate-200 hover:border-emerald-300 hover:text-emerald-700 text-slate-600 dark:bg-slate-900 dark:border-slate-800 dark:hover:border-emerald-700 dark:hover:text-emerald-300 dark:text-slate-300 transition-colors text-left shadow-2xs"
            >
              {example}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
