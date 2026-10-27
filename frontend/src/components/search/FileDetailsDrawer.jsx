import React, { useEffect } from 'react';
import {
  X,
  ExternalLink,
  Calendar,
  HardDrive,
  Folder,
  Tag,
  FileText,
  Clock,
  Sparkles,
} from 'lucide-react';
import FileTypeIcon from '../common/FileTypeIcon';
import Badge from '../common/Badge';
import {
  formatFileSize,
  formatDate,
  getFileTypeInfo,
  formatMatchedBy,
} from '../../utils/formatters';
import { getFileServeUrl } from '../../services/api';

export default function FileDetailsDrawer({
  isOpen,
  onClose,
  result,
  onOpenViewer,
}) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      document.body.style.overflow = 'unset';
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen || !result) return null;

  const fileName = result.file_name || 'Untitled Document';
  const fileType = result.file_type || 'file';
  const typeInfo = getFileTypeInfo(fileType);
  const path = result.path || result.original_uri || 'Not recorded';
  const fileSize = formatFileSize(result.file_size) || 'Unknown size';
  const modifiedDate = formatDate(result.modified_time) || 'Unknown';
  const createdDate = formatDate(result.created_time);
  const preview = result.preview || result.summary || '';
  const keywords = Array.isArray(result.keywords) ? result.keywords : [];
  const matchedBy = Array.isArray(result.matched_by) ? result.matched_by : [];
  const serveUrl = getFileServeUrl(fileType, fileName);

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs transition-opacity animate-in fade-in duration-200"
        onClick={onClose}
      />

      {/* Drawer Container */}
      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 shadow-2xl flex flex-col justify-between animate-in slide-in-from-right duration-200">
          {/* Header */}
          <div className="flex items-center justify-between p-5 border-b border-slate-100 dark:border-slate-800">
            <div className="flex items-center gap-2.5 min-w-0 pr-3">
              <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 shrink-0">
                <FileTypeIcon type={fileType} className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate" title={fileName}>
                  {fileName}
                </h3>
                <span className="text-xs text-slate-500 dark:text-slate-400">
                  {typeInfo.label}
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              aria-label="Close details"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Body Content */}
          <div className="flex-1 overflow-y-auto p-5 space-y-6">
            {/* Quick action: View file */}
            <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200/80 dark:border-slate-800 flex items-center justify-between gap-3">
              <div className="text-xs text-slate-600 dark:text-slate-300 font-medium">
                Open document preview in browser
              </div>
              <button
                type="button"
                onClick={() => onOpenViewer(result)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-600 hover:bg-emerald-700 text-white transition-colors shadow-xs"
              >
                <span>View file</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Document Attributes */}
            <div className="space-y-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                File Details
              </h4>

              <div className="space-y-2 text-xs">
                <div className="flex items-start gap-2.5 text-slate-600 dark:text-slate-300">
                  <Folder className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                  <span className="font-mono break-all text-[11px] text-slate-500 dark:text-slate-400">
                    {path}
                  </span>
                </div>

                <div className="flex items-center gap-2.5 text-slate-600 dark:text-slate-300">
                  <HardDrive className="w-4 h-4 text-slate-400 shrink-0" />
                  <span>Size: {fileSize}</span>
                </div>

                <div className="flex items-center gap-2.5 text-slate-600 dark:text-slate-300">
                  <Calendar className="w-4 h-4 text-slate-400 shrink-0" />
                  <span>Modified: {modifiedDate}</span>
                </div>

                {createdDate && (
                  <div className="flex items-center gap-2.5 text-slate-600 dark:text-slate-300">
                    <Clock className="w-4 h-4 text-slate-400 shrink-0" />
                    <span>Created: {createdDate}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Matched Signals */}
            {matchedBy.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  Match Reasons
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {matchedBy.map((m, idx) => (
                    <Badge key={idx} variant="brand" size="sm">
                      {formatMatchedBy(m)}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Content Preview */}
            <div className="space-y-2">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                Extracted Text Preview
              </h4>
              <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950/60 border border-slate-200/80 dark:border-slate-800 text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-sans whitespace-pre-wrap max-h-56 overflow-y-auto">
                {preview ? (
                  preview
                ) : (
                  <span className="italic text-slate-400 dark:text-slate-500">
                    No text preview available for this file.
                  </span>
                )}
              </div>
            </div>

            {/* Extracted Keywords */}
            {keywords.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  Detected Keywords
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {keywords.map((kw, idx) => (
                    <span
                      key={idx}
                      className="text-xs px-2.5 py-1 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200/60 dark:border-slate-700/60"
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-slate-100 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-900/50 flex items-center justify-between gap-3">
            <a
              href={serveUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 inline-flex items-center gap-1"
            >
              <span>Download raw file</span>
              <ExternalLink className="w-3 h-3" />
            </a>

            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium rounded-lg border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
