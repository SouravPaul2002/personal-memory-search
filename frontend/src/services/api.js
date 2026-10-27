import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000, // 45 seconds for heavy scanning operations
});

/**
 * Searches documents via the FastAPI /search endpoint
 * @param {string} query - natural language search query
 * @param {string} fileType - filter: 'all' | 'pdf' | 'image' | 'txt' | 'docx' | 'pptx'
 */
export const searchDocuments = async (query, fileType = 'all') => {
  try {
    const response = await apiClient.get('/search', {
      params: { q: query, type: fileType },
    });
    return response.data;
  } catch (err) {
    throw new Error(formatApiError(err, 'Search request failed'));
  }
};

/**
 * Retrieves indexing & storage status from FastAPI /status
 */
export const getSystemStatus = async () => {
  try {
    const response = await apiClient.get('/status');
    return response.data;
  } catch (err) {
    throw new Error(formatApiError(err, 'Failed to fetch system status'));
  }
};

/**
 * Uploads a document to the backend storage
 */
export const uploadDocument = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('original_uri', file.name);

  try {
    const response = await apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percent);
        }
      },
    });
    return response.data;
  } catch (err) {
    throw new Error(formatApiError(err, 'Upload failed'));
  }
};

/**
 * Triggers an incremental or full re-scan on the FastAPI backend
 */
export const triggerScan = async (type = 'incremental') => {
  const endpoint = type === 'full' ? '/scan/full' : '/scan/incremental';
  try {
    const response = await apiClient.post(endpoint);
    return response.data;
  } catch (err) {
    throw new Error(formatApiError(err, 'Index scan failed'));
  }
};

/**
 * Scans and indexes an entire directory directly from the machine
 * @param {string} folderPath - absolute directory path
 * @param {boolean} recursive - whether to scan subdirectories
 */
export const scanFolder = async (folderPath, recursive = true) => {
  try {
    const response = await apiClient.post('/scan/folder', {
      folder_path: folderPath,
      recursive,
    });
    return response.data;
  } catch (err) {
    throw new Error(formatApiError(err, 'Folder scan failed'));
  }
};

/**
 * Uploads an entire batch of files selected via browser folder picker and runs scan
 */
export const uploadFolderBatch = async (fileList, onProgress) => {
  const total = fileList.length;
  let completed = 0;
  const errors = [];

  for (let i = 0; i < total; i++) {
    const file = fileList[i];
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('original_uri', file.webkitRelativePath || file.name);

      await apiClient.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      completed++;
      if (onProgress) {
        onProgress(Math.round((completed / total) * 100), completed, total);
      }
    } catch (e) {
      errors.push(`${file.name}: ${e.message}`);
    }
  }

  // Automatically trigger an incremental scan to index all newly uploaded files
  let scanResult = null;
  try {
    scanResult = await triggerScan('incremental');
  } catch (e) {
    console.warn('Post-upload incremental scan failed:', e);
  }

  return {
    total,
    completed,
    errors,
    scanResult,
  };
};

/**
 * Constructs the direct stream URL for a file
 */
export const getFileServeUrl = (fileType, fileName) => {
  if (!fileType || !fileName) return '';
  const cleanType = fileType.toLowerCase() === 'jpg' || fileType.toLowerCase() === 'png' || fileType.toLowerCase() === 'jpeg' ? 'image' : fileType.toLowerCase();
  return `${API_BASE_URL}/files/serve/${encodeURIComponent(cleanType)}/${encodeURIComponent(fileName)}`;
};

/**
 * Formats API errors into plain-language, non-technical messages
 */
export const formatApiError = (err, defaultMsg = 'An unexpected error occurred') => {
  if (!err) return defaultMsg;

  if (err.code === 'ECONNABORTED') {
    return 'The request timed out. The backend might be busy re-indexing large documents.';
  }

  if (err.message && err.message.includes('Network Error')) {
    return 'Could not connect to the backend server. Please make sure the FastAPI server is running on http://localhost:8000.';
  }

  if (err.response) {
    const status = err.response.status;
    const detail = err.response.data?.detail || err.response.data?.message;

    if (status === 404) return detail || 'The requested file or endpoint was not found.';
    if (status === 400) return detail || 'Invalid request parameters.';
    if (status === 500) {
      return detail || 'The server encountered an error processing your request. Please try again.';
    }
    return detail || `Server returned error (${status}).`;
  }

  return err.message || defaultMsg;
};

export default apiClient;
