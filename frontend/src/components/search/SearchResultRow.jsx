import React from 'react';
import FileTypeIcon from '../common/FileTypeIcon';
import Badge from '../common/Badge';
import { formatFileSize, formatDate, formatMatchedBy } from '../../utils/formatters';
import { ChevronRight } from 'lucide-react';

export default function SearchResultRow({ result, onSelect }) {
  if (!result) return null;

  const fileName = result.file_name || 'Untitled Document';
  const fileType = result.file_type || 'file';
  const preview = result.preview || result.summary || '';
  const path = result.path || result.original_uri || '';
  const fileSize = formatFileSize(result.file_size);
  const modifiedDate = formatDate(result.modified_time);
  const matchedBy = Array.isArray(result.matched_by) ? result.matched_by : [];

  return (
    <div
      onClick={() => onSelect(result)}
      className="group flex items-start gap-3.5 p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-slate-300 dark:hover:border-slate-700 transition-all cursor-pointer shadow-xs hover:shadow-sm"
    >
      {/* File type icon */}
      <div className="shrink-0 mt-0.5 p-2 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700/80">
        <FileTypeIcon type={fileType} className="w-5 h-5" />
      </div>

      {/* Main content */}
      <div className="flex-1 min-w-0">
        {/* Title + Metadata badges row */}
        <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
          <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
            {fileName}
          </h4>

          <div className="flex items-center gap-1.5 shrink-0">
            <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400 uppercase px-1.5 py-0.5 rounded-sm bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
              {fileType}
            </span>
            {fileSize && (
              <span className="text-xs text-slate-400 dark:text-slate-500">
                • {fileSize}
              </span>
            )}
            {modifiedDate && (
              <span className="text-xs text-slate-400 dark:text-slate-500 hidden sm:inline">
                • {modifiedDate}
              </span>
            )}
          </div>
        </div>

        {/* Content Preview Snippet */}
        {preview && (
          <p className="text-xs text-slate-600 dark:text-slate-300 line-clamp-2 leading-relaxed mb-2 font-normal">
            {preview}
          </p>
        )}

        {/* Footer info: Path and Matched By Tags */}
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-slate-400 dark:text-slate-500 pt-0.5">
          {/* File location with subtle blue hint */}
          <div className="truncate max-w-md text-[11px] font-mono text-slate-500 dark:text-slate-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" title={path}>
            {path}
          </div>

          {/* Matched tags */}
          {matchedBy.length > 0 && (
            <div className="flex items-center gap-1 shrink-0">
              {matchedBy.map((tag, idx) => {
                const isSemantic = tag === 'semantic' || tag === 'vector';
                return (
                  <span
                    key={idx}
                    className={`text-[10px] px-1.5 py-0.5 rounded-md border font-medium ${
                      isSemantic
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/80'
                        : 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800/80'
                    }`}
                  >
                    {formatMatchedBy(tag)}
                  </span>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Right chevron indicator */}
      <div className="hidden sm:flex self-center pl-1 text-slate-300 dark:text-slate-600 group-hover:text-slate-500 dark:group-hover:text-slate-300 transition-colors">
        <ChevronRight className="w-4 h-4" />
      </div>
    </div>
  );
}
