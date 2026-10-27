import React, { useState } from 'react';
import SearchBar from '../components/search/SearchBar';
import SearchFilters from '../components/search/SearchFilters';
import SearchResultRow from '../components/search/SearchResultRow';
import FileDetailsDrawer from '../components/search/FileDetailsDrawer';
import DocumentViewerModal from '../components/search/DocumentViewerModal';
import { searchDocuments } from '../services/api';
import {
  Search,
  AlertCircle,
  FileQuestion,
  RefreshCw,
  Sparkles,
  Clock,
} from 'lucide-react';

export default function SearchPage({ onRecordRecentFile }) {
  const [query, setQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [results, setResults] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [searchIntent, setSearchIntent] = useState(null);
  const [queryTimeMs, setQueryTimeMs] = useState(null);
  const [status, setStatus] = useState('initial'); // 'initial' | 'loading' | 'results' | 'empty' | 'error'
  const [errorMessage, setErrorMessage] = useState('');

  // Drawer & Viewer state
  const [selectedResult, setSelectedResult] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [viewerResult, setViewerResult] = useState(null);
  const [isViewerOpen, setIsViewerOpen] = useState(false);

  const performSearch = async (searchQuery, filterType = selectedFilter) => {
    if (!searchQuery || !searchQuery.trim()) return;

    setStatus('loading');
    setErrorMessage('');
    const startTime = Date.now();

    try {
      const data = await searchDocuments(searchQuery.trim(), filterType);
      const elapsed = Date.now() - startTime;
      setQueryTimeMs(elapsed);

      const items = Array.isArray(data.results) ? data.results : [];
      setResults(items);
      setTotalCount(data.total || items.length);
      setSearchIntent(data.intent || null);

      if (items.length === 0) {
        setStatus('empty');
      } else {
        setStatus('results');
      }
    } catch (err) {
      setStatus('error');
      setErrorMessage(err.message || 'Could not complete search request.');
    }
  };

  const handleFilterChange = (newFilter) => {
    setSelectedFilter(newFilter);
    if (query.trim() && (status === 'results' || status === 'empty')) {
      performSearch(query, newFilter);
    }
  };

  const handleSelectResult = (result) => {
    setSelectedResult(result);
    setIsDrawerOpen(true);

    // Record into recent files
    if (onRecordRecentFile) {
      onRecordRecentFile(result);
    }
  };

  const handleOpenViewer = (result) => {
    setViewerResult(result);
    setIsViewerOpen(true);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-4">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          Search
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Find information across your notes, documents, and screenshots using natural language.
        </p>
      </div>

      {/* Search Input Bar */}
      <SearchBar
        query={query}
        setQuery={setQuery}
        onSearch={(q) => performSearch(q, selectedFilter)}
        isLoading={status === 'loading'}
        onSelectExample={(example) => {
          setQuery(example);
          performSearch(example, selectedFilter);
        }}
      />

      {/* Filter Chips */}
      <div className="pt-1">
        <SearchFilters
          selectedFilter={selectedFilter}
          onSelectFilter={handleFilterChange}
          disabled={status === 'loading'}
        />
      </div>

      {/* Search States Container */}
      <div className="pt-2">
        {/* State 1: Initial State */}
        {status === 'initial' && (
          <div className="py-16 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl p-8 space-y-3 bg-white/50 dark:bg-slate-900/30">
            <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center mx-auto text-slate-400">
              <Search className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Ready to search your memories
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
              Enter any concept, topic, or keyword above. The engine scans through text chunks,
              YAKE keywords, and visual image concepts simultaneously.
            </p>
          </div>
        )}

        {/* State 2: Loading State */}
        {status === 'loading' && (
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 px-1 py-2">
              <RefreshCw className="w-3.5 h-3.5 animate-spin text-slate-400" />
              <span>Searching semantic vector space and keyword indices...</span>
            </div>

            {[1, 2, 3, 4].map((n) => (
              <div
                key={n}
                className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800/80 bg-white dark:bg-slate-900/50 space-y-3 animate-pulse"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-800" />
                  <div className="flex-1 space-y-1.5">
                    <div className="w-1/3 h-4 bg-slate-200 dark:bg-slate-800 rounded" />
                    <div className="w-1/4 h-3 bg-slate-100 dark:bg-slate-800/60 rounded" />
                  </div>
                </div>
                <div className="w-full h-3 bg-slate-100 dark:bg-slate-800/60 rounded" />
                <div className="w-4/5 h-3 bg-slate-100 dark:bg-slate-800/60 rounded" />
              </div>
            ))}
          </div>
        )}

        {/* State 3: Results State */}
        {status === 'results' && (
          <div className="space-y-4">
            {/* Meta status bar */}
            <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 px-1">
              <span>
                Found <strong className="font-semibold text-slate-800 dark:text-slate-200">{totalCount}</strong> matching {totalCount === 1 ? 'file' : 'files'}
              </span>

              <div className="flex items-center gap-3 text-slate-400 dark:text-slate-500">
                {queryTimeMs !== null && (
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>{queryTimeMs} ms</span>
                  </span>
                )}
                {searchIntent && (
                  <span className="capitalize px-1.5 py-0.5 rounded-sm bg-slate-100 dark:bg-slate-800 text-[10px]">
                    {searchIntent} query
                  </span>
                )}
              </div>
            </div>

            {/* Vertical Result Rows */}
            <div className="space-y-2.5">
              {results.map((item, idx) => (
                <SearchResultRow
                  key={item.path || idx}
                  result={item}
                  onSelect={handleSelectResult}
                />
              ))}
            </div>
          </div>
        )}

        {/* State 4: Empty State */}
        {status === 'empty' && (
          <div className="py-16 text-center border border-slate-200 dark:border-slate-800 rounded-2xl p-8 space-y-3 bg-white dark:bg-slate-900/40">
            <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center mx-auto text-slate-400">
              <FileQuestion className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              No matching files found
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
              We couldn't find any documents or images matching "{query}". Try using broader
              keywords, or switch your filter to "All files".
            </p>
            {selectedFilter !== 'all' && (
              <button
                type="button"
                onClick={() => handleFilterChange('all')}
                className="mt-2 text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline"
              >
                Clear filter and search all files
              </button>
            )}
          </div>
        )}

        {/* State 5: Error State */}
        {status === 'error' && (
          <div className="p-6 border border-rose-200 dark:border-rose-900/60 bg-rose-50/60 dark:bg-rose-950/20 rounded-2xl text-center space-y-3">
            <div className="w-10 h-10 rounded-full bg-rose-100 dark:bg-rose-900/40 text-rose-600 dark:text-rose-400 flex items-center justify-center mx-auto">
              <AlertCircle className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Search request failed
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 max-w-md mx-auto mt-1 leading-relaxed">
                {errorMessage}
              </p>
            </div>
            <button
              type="button"
              onClick={() => performSearch(query, selectedFilter)}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-medium bg-emerald-600 hover:bg-emerald-700 text-white transition-colors shadow-xs"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry Search</span>
            </button>
          </div>
        )}
      </div>

      {/* Details Slide-Over Drawer */}
      <FileDetailsDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        result={selectedResult}
        onOpenViewer={handleOpenViewer}
      />

      {/* Document Viewer Modal */}
      <DocumentViewerModal
        isOpen={isViewerOpen}
        onClose={() => setIsViewerOpen(false)}
        result={viewerResult}
      />
    </div>
  );
}
