import React from 'react';
import {
  Search,
  Database,
  ArrowRight,
  FolderOpen,
  RefreshCw,
  Sparkles,
  FileText,
  Image as ImageIcon,
  ShieldCheck,
} from 'lucide-react';

export default function DashboardPage({ onNavigate }) {
  const steps = [
    {
      number: '1',
      title: 'Organize your files',
      description:
        'Place your PDFs, images, notes, Word documents, or presentations into your personal storage directories.',
      actionLabel: 'View Index Management',
      tab: 'index',
      icon: FolderOpen,
    },
    {
      number: '2',
      title: 'Update your index',
      description:
        'Run an index update whenever you add or modify files. The engine extracts text, keywords, and semantic concepts.',
      actionLabel: 'Update Index',
      tab: 'index',
      icon: RefreshCw,
    },
    {
      number: '3',
      title: 'Search with natural language',
      description:
        'Search for concepts, ideas, or topics you remember instead of memorizing exact filenames or locations.',
      actionLabel: 'Start Searching',
      tab: 'search',
      icon: Search,
    },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-10 py-4">
      {/* Welcome Hero Section */}
      <div className="space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/80 text-xs font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          <span>100% Local & Private Knowledge Engine</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-900 dark:text-slate-100 leading-tight">
          Your memories, easier to find.
        </h1>

        <p className="text-base text-slate-600 dark:text-slate-400 max-w-2xl leading-relaxed">
          Personal Memory helps you rediscover useful thoughts, documents, and screenshots
          without needing to remember specific filenames, dates, or folder hierarchies.
        </p>

        {/* Quick Action Navigation Buttons */}
        <div className="pt-2 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => onNavigate('search')}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium transition-colors shadow-xs"
          >
            <Search className="w-4 h-4" />
            <span>Search Your Files</span>
            <ArrowRight className="w-4 h-4 ml-0.5 opacity-90" />
          </button>

          <button
            type="button"
            onClick={() => onNavigate('index')}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 text-sm font-medium transition-colors shadow-xs"
          >
            <Database className="w-4 h-4 text-slate-400" />
            <span>Manage Storage & Index</span>
          </button>
        </div>
      </div>

      {/* Visual Accent Motif (Subtle, non-gradient) */}
      <div className="p-6 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="flex items-start gap-3.5">
            <div className="p-2.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-900/60 shrink-0">
              <FileText className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-0.5">
                Multi-format Documents
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Indexes text within PDFs, Word documents, PowerPoint slides, and plain text files.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3.5">
            <div className="p-2.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-900/60 shrink-0">
              <ImageIcon className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-0.5">
                Visual & Image Semantics
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Searches pictures and screenshots using visual concepts and extracted text.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3.5">
            <div className="p-2.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-900/60 shrink-0">
              <Sparkles className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-0.5">
                Semantic Meaning
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Combines dense conceptual embeddings with keywords, topics, and file titles.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Getting Started Guide */}
      <div className="space-y-4">
        <div className="border-b border-slate-100 dark:border-slate-800 pb-2">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
            How to get started
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Three simple steps to keep your local memory up to date.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {steps.map((step) => {
            const Icon = step.icon;
            return (
              <div
                key={step.number}
                className="flex flex-col justify-between p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4 hover:border-slate-300 dark:hover:border-slate-700 transition-all shadow-xs"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center justify-center w-6 h-6 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/50 dark:text-emerald-400 dark:border-emerald-800/80 text-xs font-semibold">
                      {step.number}
                    </span>
                    <Icon className="w-4 h-4 text-slate-400" />
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                    {step.title}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                    {step.description}
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => onNavigate(step.tab)}
                  className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300 inline-flex items-center gap-1 self-start transition-colors pt-1"
                >
                  <span>{step.actionLabel}</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
