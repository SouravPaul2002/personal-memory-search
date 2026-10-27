import React, { useState, useRef } from 'react';
import {
  FolderSearch,
  FolderOpen,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  FolderPlus,
  Layers,
  FileCheck,
  ChevronRight,
  HardDrive,
} from 'lucide-react';
import { scanFolder, uploadFolderBatch } from '../../services/api';

export default function FolderScannerZone({ onScanComplete }) {
  // Tab: 'path' (Direct Local Folder Path) | 'picker' (Browser Folder Selection)
  const [activeMode, setActiveMode] = useState('path');

  // Mode 1: Direct Folder Path
  const [folderPath, setFolderPath] = useState('');
  const [recursive, setRecursive] = useState(true);
  const [isScanningPath, setIsScanningPath] = useState(false);
  const [pathResult, setPathResult] = useState(null);
  const [pathError, setPathError] = useState(null);

  // Mode 2: Browser Folder Picker
  const [selectedFolderFiles, setSelectedFolderFiles] = useState([]);
  const [folderName, setFolderName] = useState('');
  const [isUploadingBatch, setIsUploadingBatch] = useState(false);
  const [batchProgress, setBatchProgress] = useState(0);
  const [batchCurrentIndex, setBatchCurrentIndex] = useState(0);
  const [batchResult, setBatchResult] = useState(null);
  const [batchError, setBatchError] = useState(null);

  const folderInputRef = useRef(null);

  const presets = [
    { label: 'data/images', path: 'data/images' },
    { label: 'data/pdfs', path: 'data/pdfs' },
    { label: 'data/txts', path: 'data/txts' },
    { label: 'data/docx', path: 'data/docx' },
    { label: 'data/pptx', path: 'data/pptx' },
  ];

  // Handler for Direct Path Scan
  const handleScanFolderPath = async (e) => {
    if (e) e.preventDefault();
    if (!folderPath.trim() || isScanningPath) return;

    setIsScanningPath(true);
    setPathResult(null);
    setPathError(null);

    try {
      const data = await scanFolder(folderPath.trim(), recursive);
      setPathResult(data);
      if (onScanComplete) {
        onScanComplete();
      }
    } catch (err) {
      setPathError(err.message || 'Failed to scan the specified directory.');
    } finally {
      setIsScanningPath(false);
    }
  };

  // Handler for Browser Folder Selection
  const handleFolderPicked = (e) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    // Filter to supported extensions
    const supportedExts = ['.jpg', '.jpeg', '.png', '.webp', '.pdf', '.txt', '.docx', '.pptx'];
    const validFiles = files.filter((f) => {
      const ext = f.name.slice(f.name.lastIndexOf('.')).toLowerCase();
      return supportedExts.includes(ext);
    });

    // Detect folder name from webkitRelativePath
    const firstRel = files[0].webkitRelativePath || '';
    const rootFolderName = firstRel.split('/')[0] || 'Selected Folder';

    setSelectedFolderFiles(validFiles);
    setFolderName(rootFolderName);
    setBatchResult(null);
    setBatchError(null);
  };

  // Handler for Batch Folder Upload & Scan
  const handleUploadFolderBatch = async () => {
    if (selectedFolderFiles.length === 0 || isUploadingBatch) return;

    setIsUploadingBatch(true);
    setBatchProgress(0);
    setBatchCurrentIndex(0);
    setBatchResult(null);
    setBatchError(null);

    try {
      const result = await uploadFolderBatch(selectedFolderFiles, (pct, current, total) => {
        setBatchProgress(pct);
        setBatchCurrentIndex(current);
      });

      setBatchResult(result);
      setSelectedFolderFiles([]);
      if (folderInputRef.current) folderInputRef.current.value = '';

      if (onScanComplete) {
        onScanComplete();
      }
    } catch (err) {
      setBatchError(err.message || 'Batch folder upload failed.');
    } finally {
      setIsUploadingBatch(false);
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-5 shadow-xs space-y-5">
      {/* Mode Switcher Tabs */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
        <div className="flex items-center space-x-1.5 p-1 bg-slate-100/80 dark:bg-slate-800 rounded-lg text-xs">
          <button
            type="button"
            onClick={() => setActiveMode('path')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-medium transition-all ${
              activeMode === 'path'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <FolderSearch className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>Direct Folder Scan (Zero-Upload)</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveMode('picker')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-medium transition-all ${
              activeMode === 'picker'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <FolderOpen className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>Pick Folder From Device</span>
          </button>
        </div>

        <span className="text-[11px] text-slate-400 dark:text-slate-500 hidden sm:inline">
          Indexes all images & documents in batch
        </span>
      </div>

      {/* MODE 1: Direct Local Directory Path Scanner */}
      {activeMode === 'path' && (
        <div className="space-y-4">
          <form onSubmit={handleScanFolderPath} className="space-y-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                Local Folder Path
              </label>
              <div className="flex items-center gap-2">
                <div className="relative flex-1">
                  <HardDrive className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
                  <input
                    type="text"
                    value={folderPath}
                    onChange={(e) => setFolderPath(e.target.value)}
                    placeholder="e.g. D:\Photos or C:\Users\sourav paul\Pictures or data/images"
                    className="w-full pl-10 pr-4 py-2.5 text-xs font-mono rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/50 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all"
                    disabled={isScanningPath}
                  />
                </div>

                <button
                  type="submit"
                  disabled={isScanningPath || !folderPath.trim()}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs font-medium bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-40 transition-colors shadow-xs shrink-0"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isScanningPath ? 'animate-spin' : ''}`} />
                  <span>{isScanningPath ? 'Scanning Folder...' : 'Scan & Index Folder'}</span>
                </button>
              </div>
            </div>

            {/* Presets and options */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-1 text-xs text-slate-500">
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="text-[11px] text-slate-400">Quick folders:</span>
                {presets.map((p) => (
                  <button
                    key={p.label}
                    type="button"
                    onClick={() => setFolderPath(p.path)}
                    className="px-2 py-0.5 rounded-md bg-slate-100 hover:bg-slate-200/70 dark:bg-slate-800 dark:hover:bg-slate-700 font-mono text-[10px] text-slate-600 dark:text-slate-300 transition-colors"
                  >
                    {p.label}
                  </button>
                ))}
              </div>

              <label className="inline-flex items-center gap-1.5 cursor-pointer text-xs text-slate-600 dark:text-slate-400 select-none">
                <input
                  type="checkbox"
                  checked={recursive}
                  onChange={(e) => setRecursive(e.target.checked)}
                  className="rounded text-emerald-600 focus:ring-emerald-500"
                />
                <span>Include subfolders recursively</span>
              </label>
            </div>
          </form>

          {/* Scanning In-progress banner */}
          {isScanningPath && (
            <div className="p-4 rounded-xl border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/50 dark:bg-emerald-950/20 text-xs text-emerald-900 dark:text-emerald-200 flex items-center gap-3">
              <RefreshCw className="w-4 h-4 animate-spin text-emerald-600 dark:text-emerald-400 shrink-0" />
              <div>
                <span className="font-semibold">Traversing and indexing directory...</span>
                <p className="text-[11px] text-emerald-700 dark:text-emerald-300 mt-0.5">
                  Scanning image concepts with CLIP, extracting document text chunks, and registering vectors.
                </p>
              </div>
            </div>
          )}

          {/* Success Result */}
          {pathResult && !isScanningPath && (
            <div className="p-4 rounded-xl border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/50 dark:bg-emerald-950/20 text-xs text-emerald-900 dark:text-emerald-200 space-y-2">
              <div className="flex items-center gap-2 font-semibold text-sm">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <span>{pathResult.message}</span>
              </div>
              <div className="pl-6 grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
                <div className="p-2 rounded-lg bg-white/60 dark:bg-slate-900/40 border border-emerald-100 dark:border-emerald-900/40">
                  <span className="text-slate-500 dark:text-slate-400 block">Total Discovered</span>
                  <span className="font-bold text-slate-900 dark:text-slate-100 text-sm">{pathResult.total_scanned}</span>
                </div>
                <div className="p-2 rounded-lg bg-white/60 dark:bg-slate-900/40 border border-emerald-100 dark:border-emerald-900/40">
                  <span className="text-slate-500 dark:text-slate-400 block">New Files Added</span>
                  <span className="font-bold text-emerald-600 dark:text-emerald-400 text-sm">+{pathResult.new_files}</span>
                </div>
                <div className="p-2 rounded-lg bg-white/60 dark:bg-slate-900/40 border border-emerald-100 dark:border-emerald-900/40">
                  <span className="text-slate-500 dark:text-slate-400 block">Updated Files</span>
                  <span className="font-bold text-slate-700 dark:text-slate-300 text-sm">{pathResult.modified_files}</span>
                </div>
                <div className="p-2 rounded-lg bg-white/60 dark:bg-slate-900/40 border border-emerald-100 dark:border-emerald-900/40">
                  <span className="text-slate-500 dark:text-slate-400 block">Unchanged (Skipped)</span>
                  <span className="font-bold text-slate-500 dark:text-slate-400 text-sm">{pathResult.skipped_files}</span>
                </div>
              </div>
            </div>
          )}

          {/* Error Result */}
          {pathError && !isScanningPath && (
            <div className="p-4 rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50/50 dark:bg-rose-950/20 text-xs text-rose-800 dark:text-rose-300 flex items-center gap-2.5">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>{pathError}</span>
            </div>
          )}
        </div>
      )}

      {/* MODE 2: Browser Folder Picker */}
      {activeMode === 'picker' && (
        <div className="space-y-4">
          <input
            ref={folderInputRef}
            type="file"
            webkitdirectory="true"
            directory="true"
            multiple
            onChange={handleFolderPicked}
            className="hidden"
          />

          {selectedFolderFiles.length === 0 ? (
            <div
              onClick={() => folderInputRef.current?.click()}
              className="p-8 border-2 border-dashed border-slate-200 dark:border-slate-800 hover:border-emerald-400 dark:hover:border-emerald-600 rounded-xl text-center cursor-pointer bg-slate-50/40 dark:bg-slate-950/30 transition-all group"
            >
              <div className="w-11 h-11 rounded-full bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto mb-2.5 group-hover:scale-105 transition-transform">
                <FolderOpen className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Click to Select an Entire Folder
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto mt-1 leading-relaxed">
                Choose any folder from your computer. All images, PDFs, Word docs, and notes inside will be selected at once.
              </p>
            </div>
          ) : (
            <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950/40 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600">
                    <FolderPlus className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                      Folder: "{folderName}"
                    </h4>
                    <span className="text-xs text-slate-500 dark:text-slate-400">
                      {selectedFolderFiles.length} supported files ready for batch indexing
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedFolderFiles([]);
                      if (folderInputRef.current) folderInputRef.current.value = '';
                    }}
                    disabled={isUploadingBatch}
                    className="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 text-xs font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                  >
                    Change Folder
                  </button>

                  <button
                    type="button"
                    onClick={handleUploadFolderBatch}
                    disabled={isUploadingBatch}
                    className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-xs font-medium bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs disabled:opacity-40 transition-colors"
                  >
                    <RefreshCw className={`w-3.5 h-3.5 ${isUploadingBatch ? 'animate-spin' : ''}`} />
                    <span>
                      {isUploadingBatch
                        ? `Processing ${batchCurrentIndex}/${selectedFolderFiles.length}...`
                        : 'Upload & Index All Files'}
                    </span>
                  </button>
                </div>
              </div>

              {/* Upload Progress Bar */}
              {isUploadingBatch && (
                <div className="space-y-1.5 pt-2">
                  <div className="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                    <span>Uploading and vectorizing files...</span>
                    <span>{batchProgress}%</span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div
                      className="bg-emerald-500 h-1.5 rounded-full transition-all duration-150"
                      style={{ width: `${batchProgress}%` }}
                    />
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Batch Result */}
          {batchResult && !isUploadingBatch && (
            <div className="p-4 rounded-xl border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/50 dark:bg-emerald-950/20 text-xs text-emerald-900 dark:text-emerald-200 space-y-1">
              <div className="flex items-center gap-2 font-semibold">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <span>Batch folder indexing complete!</span>
              </div>
              <p className="text-[11px] pl-6 text-emerald-700 dark:text-emerald-300">
                Successfully processed <strong>{batchResult.completed}</strong> files. Content chunks and CLIP embeddings have been refreshed.
              </p>
            </div>
          )}

          {/* Batch Error */}
          {batchError && !isUploadingBatch && (
            <div className="p-4 rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50/50 dark:bg-rose-950/20 text-xs text-rose-800 dark:text-rose-300 flex items-center gap-2.5">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>{batchError}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
