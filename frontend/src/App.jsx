import React, { useState, useEffect } from 'react';
import Sidebar from './components/layout/Sidebar';
import DashboardPage from './pages/DashboardPage';
import SearchPage from './pages/SearchPage';
import IndexManagementPage from './pages/IndexManagementPage';
import RecentFilesPage from './pages/RecentFilesPage';
import { Menu } from 'lucide-react';

export default function App() {
  // Navigation tab: 'dashboard' | 'search' | 'index' | 'recent'
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isOpenMobile, setIsOpenMobile] = useState(false);

  // Theme state: 'light' | 'dark'
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('pm_theme');
    if (saved === 'light' || saved === 'dark') return saved;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  });

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('pm_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  // Recent files history (persisted in localStorage, max 50 items)
  const [recentFiles, setRecentFiles] = useState(() => {
    try {
      const saved = localStorage.getItem('pm_recent_files');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const recordRecentFile = (file) => {
    if (!file) return;
    setRecentFiles((prev) => {
      const fileId = file.path || file.file_name;
      const filtered = prev.filter((item) => (item.path || item.file_name) !== fileId);
      // Clean copy without heavy text blobs to keep local storage light
      const entry = {
        file_name: file.file_name,
        file_type: file.file_type,
        path: file.path,
        file_size: file.file_size,
        modified_time: file.modified_time,
        created_time: file.created_time,
        original_uri: file.original_uri,
        preview: file.preview ? file.preview.slice(0, 300) : '',
        keywords: Array.isArray(file.keywords) ? file.keywords.slice(0, 10) : [],
        matched_by: file.matched_by || [],
        viewedAt: Date.now(),
      };
      const updated = [entry, ...filtered].slice(0, 50);
      try {
        localStorage.setItem('pm_recent_files', JSON.stringify(updated));
      } catch (e) {
        console.warn('Could not persist recent files:', e);
      }
      return updated;
    });
  };

  const clearRecentHistory = () => {
    setRecentFiles([]);
    localStorage.removeItem('pm_recent_files');
  };

  return (
    <div className="min-h-screen flex bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        theme={theme}
        toggleTheme={toggleTheme}
        isOpenMobile={isOpenMobile}
        setIsOpenMobile={setIsOpenMobile}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile Top Header */}
        <header className="md:hidden flex items-center justify-between px-4 py-3 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 sticky top-0 z-30">
          <button
            type="button"
            onClick={() => setIsOpenMobile(true)}
            className="p-1.5 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
            aria-label="Open navigation menu"
          >
            <Menu className="w-5 h-5" />
          </button>
          <span className="text-sm font-semibold tracking-tight text-slate-900 dark:text-slate-100">
            Personal Memory
          </span>
          <div className="w-6" /> {/* Balance spacer */}
        </header>

        {/* Page Container */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
          {activeTab === 'dashboard' && (
            <DashboardPage onNavigate={(tab) => setActiveTab(tab)} />
          )}

          {activeTab === 'search' && (
            <SearchPage onRecordRecentFile={recordRecentFile} />
          )}

          {activeTab === 'index' && <IndexManagementPage />}

          {activeTab === 'recent' && (
            <RecentFilesPage
              recentFiles={recentFiles}
              onClearHistory={clearRecentHistory}
            />
          )}
        </main>
      </div>
    </div>
  );
}
