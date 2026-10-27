import React, { useState } from 'react';
import Modal from '../common/Modal';
import FileTypeIcon from '../common/FileTypeIcon';
import { getFileServeUrl } from '../../services/api';
import { ExternalLink, Download, AlertCircle, FileSpreadsheet, Presentation } from 'lucide-react';

export default function DocumentViewerModal({ isOpen, onClose, result }) {
  const [loadError, setLoadError] = useState(false);

  if (!isOpen || !result) return null;

  const fileName = result.file_name || 'Document';
  const fileType = (result.file_type || '').toLowerCase();
  const serveUrl = getFileServeUrl(fileType, fileName);

  return (
    <Modal
      isOpen={isOpen}
      onClose={() => {
        setLoadError(false);
        onClose();
      }}
      title={fileName}
      maxWidth="max-w-4xl"
    >
      <div className="space-y-4">
        {/* Render based on file type */}
        {loadError ? (
          <div className="p-8 text-center border border-dashed border-slate-300 dark:border-slate-700 rounded-xl space-y-3">
            <AlertCircle className="w-8 h-8 text-amber-500 mx-auto" />
            <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Inline preview could not be loaded
            </h4>
            <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
              The file may not exist in the backend data directory or is not supported for inline display.
            </p>
            <a
              href={serveUrl}
              download={fileName}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium rounded-lg bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 hover:opacity-90 transition-opacity"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download File Instead</span>
            </a>
          </div>
        ) : fileType === 'pdf' ? (
          <div className="w-full h-[65vh] rounded-lg border border-slate-200 dark:border-slate-800 overflow-hidden bg-slate-100 dark:bg-slate-950">
            <iframe
              src={serveUrl}
              title={fileName}
              className="w-full h-full border-0"
              onError={() => setLoadError(true)}
            />
          </div>
        ) : fileType === 'image' || ['jpg', 'jpeg', 'png', 'webp'].includes(fileType) ? (
          <div className="flex items-center justify-center p-4 bg-slate-100 dark:bg-slate-950/60 rounded-xl border border-slate-200 dark:border-slate-800 max-h-[65vh] overflow-hidden">
            <img
              src={serveUrl}
              alt={fileName}
              className="max-h-[60vh] max-w-full object-contain rounded-lg shadow-sm"
              onError={() => setLoadError(true)}
            />
          </div>
        ) : fileType === 'txt' ? (
          <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 text-xs font-mono text-slate-800 dark:text-slate-200 max-h-[60vh] overflow-y-auto whitespace-pre-wrap leading-relaxed">
            {result.preview || 'No text snippet preview available.'}
          </div>
        ) : (
          /* Word (docx) or PowerPoint (pptx) */
          <div className="p-8 text-center border border-slate-200 dark:border-slate-800 rounded-xl bg-slate-50/50 dark:bg-slate-800/30 space-y-4">
            <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center mx-auto">
              <FileTypeIcon type={fileType} className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-1">
                {fileType.toUpperCase()} Document
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 max-w-md mx-auto">
                Web browsers cannot natively preview binary Office formats ({fileType.toUpperCase()}) without third-party cloud viewers. You can open or download the original file to view it locally.
              </p>
            </div>
            <div className="pt-2">
              <a
                href={serveUrl}
                download={fileName}
                className="inline-flex items-center gap-2 px-4 py-2 text-xs font-medium rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white transition-colors shadow-xs"
              >
                <Download className="w-4 h-4" />
                <span>Download & Open in System App</span>
              </a>
            </div>
          </div>
        )}

        {/* Modal Footer Link */}
        <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100 dark:border-slate-800">
          <span className="truncate max-w-xs font-mono text-[11px]">
            {result.path || fileName}
          </span>
          <div className="flex items-center gap-2">
            <a
              href={serveUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-slate-600 hover:text-emerald-600 dark:text-slate-400 dark:hover:text-emerald-400 font-medium"
            >
              <span>Open in new tab</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </div>
    </Modal>
  );
}
