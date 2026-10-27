import React, { useState, useEffect, useCallback } from 'react';
import {
  RefreshCw,
  Database,
  Layers,
  FileText,
  Image as ImageIcon,
  Files,
  Clock,
  AlertTriangle,
  CheckCircle2,
  AlertCircle,
  FolderLock,
  Upload,
  FolderSearch,
} from 'lucide-react';
import Modal from '../components/common/Modal';
import FolderScannerZone from '../components/upload/FolderScannerZone';
import { getSystemStatus, triggerScan } from '../services/api';
import { formatDate } from '../utils/formatters';

export default function IndexManagementPage() {
  const [statusData, setStatusData] = useState(null);
  const [isLoadingStatus, setIsLoadingStatus] = useState(true);
  const [statusError, setStatusError] = useState(null);

  // Scan execution state
  const [isScanning, setIsScanning] = useState(false);
  const [activeScanType, setActiveScanType] = useState(null); // 'incremental' | 'full'
  const [scanResult, setScanResult] = useState(null); // { message, new_files, modified_files, deleted_files }
  const [scanError, setScanError] = useState(null);

  // Full Rebuild Confirmation Modal state
  const [isRebuildModalOpen, setIsRebuildModalOpen] = useState(false);

  // Fetch status callback
  const fetchStatus = useCallback(async () => {
    setIsLoadingStatus(true);
    setStatusError(null);
    try {
      const data = await getSystemStatus();
      setStatusData(data);
    } catch (err) {
      setStatusError(err.message || 'Could not load index status.');
    } finally {
      setIsLoadingStatus(false);
    }
  }, []);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  // Execute scan
  const handleExecuteScan = async (type) => {
    setIsScanning(true);
    setActiveScanType(type);
    setScanResult(null);
    setScanError(null);
    if (type === 'full') {
      setIsRebuildModalOpen(false);
    }

    try {
      const result = await triggerScan(type);
      setScanResult(result);
      // Refresh status after scan finishes
      await fetchStatus();
    } catch (err) {
      setScanError(err.message || `Failed to complete ${type} scan.`);
    } finally {
      setIsScanning(false);
      setActiveScanType(null);
    }
  };

  const totalFiles = statusData?.total_files ?? 0;
  const indexedChunks = statusData?.indexed_chunks ?? 0;
  const pdfCount = statusData?.pdfs ?? statusData?.indexed_pdfs ?? 0;
  const imageCount = statusData?.images ?? statusData?.indexed_images ?? 0;
  const otherDocs = (statusData?.txt ?? 0) + (statusData?.docx ?? 0) + (statusData?.pptx ?? 0);
  const lastScanTime = formatDate(statusData?.last_scan_time) || 'No scan recorded yet';
  const lastScanType = statusData?.last_scan_type ? `${statusData.last_scan_type} scan` : null;

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      {/* Page Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          Index Management
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Review your local index status, scan for document modifications, and rebuild semantic collections.
        </p>
      </div>

      {/* Overview Statistics Section */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
            Index Overview
          </h2>
          <button
            type="button"
            onClick={fetchStatus}
            disabled={isLoadingStatus || isScanning}
            className="inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoadingStatus ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>

        {statusError ? (
          <div className="p-4 rounded-xl border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 text-xs text-rose-700 dark:text-rose-300 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{statusError}</span>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3.5">
            {/* Stat 1: Total Files */}
            <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-all flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  Total Files
                </span>
                <div className="w-7 h-7 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                  <Files className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-2">
                {isLoadingStatus ? '...' : totalFiles}
              </div>
            </div>

            {/* Stat 2: Chunks */}
            <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-all flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  Content Chunks
                </span>
                <div className="w-7 h-7 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                  <Layers className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-2">
                {isLoadingStatus ? '...' : indexedChunks}
              </div>
            </div>

            {/* Stat 3: PDFs */}
            <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-all flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  PDF Documents
                </span>
                <div className="w-7 h-7 rounded-lg bg-rose-50 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400 flex items-center justify-center">
                  <FileText className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-2">
                {isLoadingStatus ? '...' : pdfCount}
              </div>
            </div>

            {/* Stat 4: Images */}
            <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-all flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  Images
                </span>
                <div className="w-7 h-7 rounded-lg bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 flex items-center justify-center">
                  <ImageIcon className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-2">
                {isLoadingStatus ? '...' : imageCount}
              </div>
            </div>

            {/* Stat 5: Other Docs */}
            <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-all flex flex-col justify-between col-span-2 sm:col-span-1">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  Other Documents
                </span>
                <div className="w-7 h-7 rounded-lg bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                  <Database className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-2">
                {isLoadingStatus ? '...' : otherDocs}
              </div>
            </div>
          </div>
        )}

        {/* Last Scan Info Bar */}
        <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 px-1 pt-1">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>Last index update: {lastScanTime}</span>
          {lastScanType && (
            <span className="px-1.5 py-0.5 rounded-sm bg-slate-100 dark:bg-slate-800 text-[10px] uppercase font-mono">
              {lastScanType}
            </span>
          )}
        </div>
      </div>

      {/* Scan Feedback Banners */}
      {isScanning && (
        <div className="p-4 rounded-xl border border-brand-200 dark:border-brand-900/60 bg-brand-50/50 dark:bg-sky-950/20 text-xs text-brand-800 dark:text-sky-300 flex items-center gap-3">
          <RefreshCw className="w-4 h-4 animate-spin text-brand-600 dark:text-sky-400 shrink-0" />
          <div>
            <span className="font-semibold">
              {activeScanType === 'full' ? 'Running full index rebuild...' : 'Updating search index...'}
            </span>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
              The engine is computing SHA-256 hashes, extracting document text, and generating dense embeddings.
            </p>
          </div>
        </div>
      )}

      {scanResult && !isScanning && (
        <div className="p-4 rounded-xl border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/50 dark:bg-emerald-950/20 text-xs text-emerald-900 dark:text-emerald-200 space-y-1">
          <div className="flex items-center gap-2 font-semibold">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>{scanResult.message || 'Scan completed successfully.'}</span>
          </div>
          <div className="pl-6 text-[11px] text-emerald-700 dark:text-emerald-300 flex flex-wrap gap-4">
            <span>• <strong>{scanResult.new_files ?? 0}</strong> new files added</span>
            <span>• <strong>{scanResult.modified_files ?? 0}</strong> files updated</span>
            <span>• <strong>{scanResult.deleted_files ?? 0}</strong> files removed</span>
          </div>
        </div>
      )}

      {scanError && !isScanning && (
        <div className="p-4 rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50/50 dark:bg-rose-950/20 text-xs text-rose-800 dark:text-rose-300 flex items-center gap-2.5">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{scanError}</span>
        </div>
      )}

      {/* Scan Actions Section */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
          Scan & Index Actions
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Action 1: Update Index */}
          <div className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800/80 bg-white dark:bg-slate-900/50 space-y-3 flex flex-col justify-between">
            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-slate-900 dark:text-slate-100 font-semibold text-sm">
                <RefreshCw className="w-4 h-4 text-brand-500" />
                <span>Update Index</span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Check for new, changed, or removed files and refresh your index. Fast and non-destructive.
              </p>
            </div>

            <button
              type="button"
              disabled={isScanning}
              onClick={() => handleExecuteScan('incremental')}
              className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-xs font-medium bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-40 transition-colors shadow-xs self-start"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isScanning && activeScanType === 'incremental' ? 'animate-spin' : ''}`} />
              <span>{isScanning && activeScanType === 'incremental' ? 'Updating...' : 'Update Index'}</span>
            </button>
          </div>

          {/* Action 2: Full Rebuild */}
          <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs space-y-3 flex flex-col justify-between">
            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-slate-900 dark:text-slate-100 font-semibold text-sm">
                <AlertTriangle className="w-4 h-4 text-amber-500" />
                <span>Full Rebuild</span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Rebuild your search index from the files currently available to the indexer. Clears old vector collections.
              </p>
            </div>

            <button
              type="button"
              disabled={isScanning}
              onClick={() => setIsRebuildModalOpen(true)}
              className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-xs font-medium border border-rose-200 dark:border-rose-900 text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 disabled:opacity-40 transition-colors self-start shadow-2xs"
            >
              <AlertTriangle className="w-3.5 h-3.5" />
              <span>Full Rebuild...</span>
            </button>
          </div>
        </div>
      </div>

      {/* Storage Folder Limitations Notice */}
      <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs text-xs text-slate-600 dark:text-slate-400 flex items-start gap-3">
        <FolderLock className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <span className="font-semibold text-slate-900 dark:text-slate-100">
            Flexible Storage & Folder Support
          </span>
          <p className="text-[11px] leading-relaxed">
            Personal Memory indexes files from its dedicated storage folders (<code className="font-mono text-slate-700 dark:text-slate-300">data/images</code>, <code className="font-mono text-slate-700 dark:text-slate-300">data/pdfs</code>, etc.) as well as <strong>any custom directory on your computer</strong> using the Folder Scan tool below.
          </p>
        </div>
      </div>

      {/* Folder Scan & Ingestion Section */}
      <div className="space-y-3 pt-2">
        <div className="border-b border-slate-100 dark:border-slate-800 pb-2">
          <div className="flex items-center gap-2">
            <FolderSearch className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
              Folder Scan & Batch Ingestion
            </h2>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Scan any local folder on your computer directly, or select a folder to index collections of images and documents without dragging files one by one.
          </p>
        </div>

        <FolderScannerZone onScanComplete={fetchStatus} />
      </div>

      {/* Full Rebuild Confirmation Dialog */}
      <Modal
        isOpen={isRebuildModalOpen}
        onClose={() => setIsRebuildModalOpen(false)}
        title="Confirm Full Index Rebuild"
      >
        <div className="space-y-4 text-xs text-slate-600 dark:text-slate-300">
          <div className="p-3 rounded-lg bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 text-amber-800 dark:text-amber-300 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-amber-600" />
            <p className="leading-relaxed">
              This action will delete all existing vector embeddings and SQLite file records before
              performing a clean scan of your data folders.
            </p>
          </div>

          <p className="leading-relaxed">
            Are you sure you want to proceed? Depending on the number of documents in your storage folder,
            a full rebuild may take several seconds.
          </p>

          <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button
              type="button"
              onClick={() => setIsRebuildModalOpen(false)}
              className="px-3.5 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={() => handleExecuteScan('full')}
              className="px-3.5 py-2 rounded-lg bg-rose-600 hover:bg-rose-700 text-white font-medium transition-colors"
            >
              Yes, Rebuild Everything
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
