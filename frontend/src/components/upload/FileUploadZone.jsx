import React, { useState, useRef } from 'react';
import { Upload, CheckCircle2, AlertCircle, FileUp, X } from 'lucide-react';
import { uploadDocument } from '../../services/api';

export default function FileUploadZone({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null); // { type: 'success' | 'error', text: '' }
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const supportedExtensions = '.pdf, .jpg, .jpeg, .png, .webp, .txt, .docx, .pptx';

  const handleFileSelection = (selectedFile) => {
    if (!selectedFile) return;
    setFile(selectedFile);
    setStatusMessage(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleUploadSubmit = async () => {
    if (!file || isUploading) return;
    setIsUploading(true);
    setProgress(0);
    setStatusMessage(null);

    try {
      const response = await uploadDocument(file, (percent) => {
        setProgress(percent);
      });

      if (response.success) {
        setStatusMessage({
          type: 'success',
          text: `"${file.name}" was uploaded successfully to backend storage. Remember to click "Update Index" to make its contents searchable!`,
        });
        setFile(null);
        if (fileInputRef.current) fileInputRef.current.value = '';
        if (onUploadSuccess) onUploadSuccess();
      } else {
        setStatusMessage({
          type: 'error',
          text: response.message || 'File upload was rejected by the server.',
        });
      }
    } catch (err) {
      setStatusMessage({
        type: 'error',
        text: err.message || 'Failed to upload document. Please ensure the backend is running.',
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Drop area */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`p-6 border-2 border-dashed rounded-xl text-center cursor-pointer transition-colors ${
          isDragging
            ? 'border-emerald-500 bg-emerald-50/50 dark:bg-emerald-950/20'
            : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-900 shadow-xs'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={supportedExtensions}
          onChange={(e) => handleFileSelection(e.target.files[0])}
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center space-y-2">
          <div className="w-10 h-10 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <Upload className="w-5 h-5" />
          </div>
          <div className="text-xs text-slate-700 dark:text-slate-300">
            <span className="font-semibold text-emerald-600 dark:text-emerald-400">Click to upload</span> or drag and drop
          </div>
          <p className="text-[11px] text-slate-400 dark:text-slate-500">
            PDF, Images, TXT, DOCX, or PPTX
          </p>
        </div>
      </div>

      {/* Selected file preview & action */}
      {file && (
        <div className="flex items-center justify-between p-3.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 shadow-2xs">
          <div className="flex items-center gap-2.5 min-w-0 pr-3">
            <FileUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
            <div className="truncate text-xs font-medium text-slate-800 dark:text-slate-200">
              {file.name}
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <button
              type="button"
              disabled={isUploading}
              onClick={() => setFile(null)}
              className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              title="Remove"
            >
              <X className="w-4 h-4" />
            </button>
            <button
              type="button"
              disabled={isUploading}
              onClick={handleUploadSubmit}
              className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-50 transition-colors shadow-xs"
            >
              {isUploading ? `Uploading ${progress}%...` : 'Upload to Storage'}
            </button>
          </div>
        </div>
      )}

      {/* Progress Bar */}
      {isUploading && (
        <div className="w-full bg-slate-100 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">
          <div
            className="bg-emerald-500 h-1.5 rounded-full transition-all duration-200"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {/* Notification banner */}
      {statusMessage && (
        <div
          className={`flex items-start gap-2.5 p-3.5 rounded-xl border text-xs leading-relaxed ${
            statusMessage.type === 'success'
              ? 'bg-emerald-50 dark:bg-emerald-950/30 border-emerald-200 dark:border-emerald-800/80 text-emerald-800 dark:text-emerald-300'
              : 'bg-rose-50 dark:bg-rose-950/30 border-rose-200 dark:border-rose-800/80 text-rose-800 dark:text-rose-300'
          }`}
        >
          {statusMessage.type === 'success' ? (
            <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5" />
          ) : (
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          )}
          <span>{statusMessage.text}</span>
        </div>
      )}
    </div>
  );
}
