import React from 'react';
import {
  Home,
  Search,
  Database,
  Clock,
  Sun,
  Moon,
  Compass,
  X,
} from 'lucide-react';

export default function Sidebar({
  activeTab,
  setActiveTab,
  theme,
  toggleTheme,
  isOpenMobile,
  setIsOpenMobile,
}) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'search', label: 'Search', icon: Search },
    { id: 'index', label: 'Index Management', icon: Database },
    { id: 'recent', label: 'Recent Files', icon: Clock },
  ];

  const handleNavClick = (id) => {
    setActiveTab(id);
    if (setIsOpenMobile) {
      setIsOpenMobile(false);
    }
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpenMobile && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/50 backdrop-blur-xs md:hidden"
          onClick={() => setIsOpenMobile(false)}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed md:sticky top-0 left-0 z-40 h-screen w-64 flex-col justify-between border-r border-slate-200 dark:border-slate-800/80 bg-white dark:bg-slate-900/90 transition-transform duration-200 md:translate-x-0 ${
          isOpenMobile ? 'translate-x-0 flex' : '-translate-x-full md:flex'
        }`}
      >
        {/* Top: Logo & Nav items */}
        <div className="flex flex-col p-4">
          {/* Logo / Header */}
          <div className="flex items-center justify-between pb-5 pt-1 px-2 border-b border-slate-200 dark:border-slate-800/80">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-emerald-600 text-white shadow-xs">
                <Compass className="w-5 h-5" />
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5">
                  <span className="text-sm font-bold tracking-tight text-slate-900 dark:text-slate-100">
                    Personal Memory
                  </span>
                  <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/50 dark:text-emerald-400 dark:border-emerald-800/80">
                    Local
                  </span>
                </div>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">
                  Document Knowledge Engine
                </span>
              </div>
            </div>

            {/* Mobile close button */}
            <button
              type="button"
              onClick={() => setIsOpenMobile(false)}
              className="p-1 rounded-md text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 md:hidden"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="mt-4 flex flex-col gap-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => handleNavClick(item.id)}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-800 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/60 shadow-xs'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100/70 dark:hover:bg-slate-800/60 border border-transparent'
                  }`}
                >
                  <Icon
                    className={`w-4 h-4 ${
                      isActive
                        ? 'text-emerald-600 dark:text-emerald-400'
                        : 'text-slate-400 dark:text-slate-500'
                    }`}
                  />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Bottom: Theme Toggle & Unobtrusive App Identity */}
        <div className="p-4 border-t border-slate-100 dark:border-slate-800/60 flex flex-col gap-3">
          {/* Theme Toggle */}
          <button
            type="button"
            onClick={toggleTheme}
            className="flex items-center justify-between w-full px-3 py-2 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <span className="flex items-center gap-2">
              {theme === 'dark' ? (
                <Moon className="w-4 h-4 text-slate-400" />
              ) : (
                <Sun className="w-4 h-4 text-amber-500" />
              )}
              <span>{theme === 'dark' ? 'Dark theme' : 'Light theme'}</span>
            </span>
            <span className="text-[11px] text-slate-400 dark:text-slate-500">
              Toggle
            </span>
          </button>

          {/* Unobtrusive Identity Section */}
          <div className="px-3 pt-1 flex items-center justify-between text-[11px] text-slate-400 dark:text-slate-500">
            <span>Offline & Local</span>
            <span className="inline-flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Ready
            </span>
          </div>
        </div>
      </aside>
    </>
  );
}
