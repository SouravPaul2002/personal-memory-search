/**
 * Formatting utilities for Personal Memory Search
 */

export const formatFileSize = (sizeInMb) => {
  if (sizeInMb === null || sizeInMb === undefined || isNaN(sizeInMb)) {
    return null;
  }
  const mb = parseFloat(sizeInMb);
  if (mb === 0) return '0 KB';
  if (mb < 0.1) {
    return `${Math.round(mb * 1024)} KB`;
  }
  if (mb < 1) {
    return `${(mb * 1024).toFixed(0)} KB`;
  }
  return `${mb.toFixed(1)} MB`;
};

export const formatDate = (dateValue) => {
  if (!dateValue || dateValue === 'Unknown') return null;

  try {
    let date;
    if (typeof dateValue === 'number') {
      // Unix epoch timestamp (seconds)
      date = new Date(dateValue * 1000);
    } else {
      date = new Date(dateValue);
    }

    if (isNaN(date.getTime())) {
      return String(dateValue);
    }

    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return `Today at ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }
    if (diffDays === 1) {
      return `Yesterday at ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }
    if (diffDays < 7) {
      return `${diffDays} days ago`;
    }

    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return String(dateValue);
  }
};

export const getFileTypeInfo = (type) => {
  const normalized = (type || '').toLowerCase();
  switch (normalized) {
    case 'pdf':
      return {
        label: 'PDF Document',
        shortLabel: 'PDF',
        colorClass: 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40 border-rose-200 dark:border-rose-900',
      };
    case 'image':
    case 'jpg':
    case 'jpeg':
    case 'png':
    case 'webp':
      return {
        label: 'Image',
        shortLabel: 'IMG',
        colorClass: 'text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 border-amber-200 dark:border-amber-900',
      };
    case 'docx':
    case 'doc':
      return {
        label: 'Word Document',
        shortLabel: 'DOC',
        colorClass: 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/40 border-blue-200 dark:border-blue-900',
      };
    case 'pptx':
    case 'ppt':
      return {
        label: 'PowerPoint',
        shortLabel: 'PPT',
        colorClass: 'text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-950/40 border-orange-200 dark:border-orange-900',
      };
    case 'txt':
      return {
        label: 'Text File',
        shortLabel: 'TXT',
        colorClass: 'text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-900',
      };
    default:
      return {
        label: 'Document',
        shortLabel: 'DOC',
        colorClass: 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700',
      };
  }
};

export const formatMatchedBy = (tag) => {
  const map = {
    embedding: 'Semantic match',
    keyword: 'Keyword match',
    filename: 'Title match',
    metadata: 'Topic match',
  };
  return map[tag] || tag;
};
