import React from 'react';
import {
  Layers,
  FileText,
  Image as ImageIcon,
  FileCode,
  FileSpreadsheet,
  Presentation,
} from 'lucide-react';

export default function SearchFilters({ selectedFilter, onSelectFilter, disabled }) {
  const filters = [
    { id: 'all', label: 'All files', icon: Layers },
    { id: 'pdf', label: 'PDFs', icon: FileText },
    { id: 'image', label: 'Images', icon: ImageIcon },
    { id: 'txt', label: 'Text files', icon: FileCode },
    { id: 'docx', label: 'Word documents', icon: FileSpreadsheet },
    { id: 'pptx', label: 'PowerPoint', icon: Presentation },
  ];

  return (
    <div className="flex flex-wrap items-center gap-1.5 py-1">
      {filters.map((f) => {
        const Icon = f.icon;
        const isSelected = selectedFilter === f.id;
        return (
          <button
            key={f.id}
            type="button"
            disabled={disabled}
            onClick={() => onSelectFilter(f.id)}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
              isSelected
                ? 'bg-emerald-50 border-emerald-300 text-emerald-800 dark:bg-emerald-950/50 dark:border-emerald-700 dark:text-emerald-300 font-semibold shadow-xs'
                : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300 dark:hover:border-slate-700 hover:text-slate-900 dark:hover:text-slate-200 shadow-2xs'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            <Icon
              className={`w-3.5 h-3.5 ${
                isSelected ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-400 dark:text-slate-500'
              }`}
            />
            <span>{f.label}</span>
          </button>
        );
      })}
    </div>
  );
}
