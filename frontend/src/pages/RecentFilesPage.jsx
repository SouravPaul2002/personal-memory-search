import React, { useState } from 'react';
import {
  Clock,
  Trash2,
  ExternalLink,
  Folder,
  Calendar,
  HardDrive,
  FileSearch,
} from 'lucide-react';
import FileTypeIcon from '../components/common/FileTypeIcon';
import FileDetailsDrawer from '../components/search/FileDetailsDrawer';
import DocumentViewerModal from '../components/search/DocumentViewerModal';
import { formatFileSize, formatDate } from '../utils/formatters';

export default function RecentFilesPage({ recentFiles, onClearHistory }) {
  const [selectedResult, setSelectedResult] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [viewerResult, setViewerResult] = useState(null);
  const [isViewerOpen, setIsViewerOpen] = useState(false);

  const handleOpenDetails = (file) => {
    setSelectedResult(file);
    setIsDrawerOpen(true);
  };

  const handleOpenViewer = (file) => {
    setViewerResult(file);
    setIsViewerOpen(true);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Recent Files
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Documents and images you have recently viewed or inspected in Personal Memory.
          </p>
        </div>

        {recentFiles && recentFiles.length > 0 && (
          <button
            type="button"
            onClick={onClearHistory}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 text-xs font-medium text-slate-600 dark:text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 hover:border-rose-200 dark:hover:border-rose-900 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear History</span>
          </button>
        )}
      </div>

      {/* Scope Disclaimer */}
      <div className="p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-800/80 bg-slate-50/60 dark:bg-slate-900/40 text-xs text-slate-500 dark:text-slate-400 flex items-center gap-2">
        <Clock className="w-4 h-4 text-slate-400 shrink-0" />
        <span>
          This list tracks files you inspect in Personal Memory. It is stored safely in your browser and limited to the last 50 viewed items.
        </span>
      </div>

      {/* List or Empty State */}
      {recentFiles && recentFiles.length > 0 ? (
        <div className="space-y-2">
          {recentFiles.map((file, idx) => {
            const fileName = file.file_name || 'Untitled';
            const fileType = file.file_type || 'file';
            const path = file.path || file.original_uri || '';
            const size = formatFileSize(file.file_size);
            const viewTime = formatDate(file.viewedAt);

            return (
              <div
                key={file.path || idx}
                onClick={() => handleOpenDetails(file)}
                className="group flex items-center justify-between gap-4 p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-slate-300 dark:hover:border-slate-700 transition-all cursor-pointer shadow-xs"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="p-2 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700/80 shrink-0">
                    <FileTypeIcon type={fileType} className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                      {fileName}
                    </h4>
                    <div className="flex items-center gap-2 text-xs text-slate-400 dark:text-slate-500 truncate mt-0.5">
                      <span className="truncate font-mono text-[11px] max-w-xs">{path}</span>
                      {size && <span>• {size}</span>}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0 text-xs text-slate-400 dark:text-slate-500">
                  {viewTime && <span>Viewed {viewTime}</span>}
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleOpenViewer(file);
                    }}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                    title="Open Viewer"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="py-16 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl p-8 space-y-3 bg-white/50 dark:bg-slate-900/30">
          <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center mx-auto text-slate-400">
            <FileSearch className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
            No recent files viewed yet
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
            When you search and inspect files in Personal Memory, they will automatically appear here
            for quick access.
          </p>
        </div>
      )}

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
