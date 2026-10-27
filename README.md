# Personal Memory Search Engine

Personal Memory Search Engine is a local, privacy-focused search application designed to help users quickly find personal documents and images. It combines natural-language semantic text search, visual similarity search, and optical character recognition (OCR) so you can locate files based on their meaning, visual content, or extracted text rather than relying strictly on exact keywords or file names.

---

## Features

- **Natural-Language File Search**: Query your documents and pictures using everyday language and descriptive phrases.
- **Semantic Text Search**: Generates dense vector embeddings using Sentence Transformers (`all-MiniLM-L6-v2`) to find documents by topical meaning.
- **Image Similarity Search**: Computes visual embeddings using OpenCLIP (`ViT-B-32`) to find images matching visual concepts and queries.
- **Hybrid Search**: Fuses text and visual search results with query intent detection to balance text documents and relevant images.
- **OCR-Based Text Extraction**: Extracts text from images (`PNG`, `JPG`, `WEBP`) using Tesseract OCR for text-based image retrieval.
- **Multi-Format Document Indexing**: Parses and extracts content from `PDF`, `TXT`, `MD`, `DOCX`, and `PPTX` files.
- **File Uploads & Custom-Folder Scanning**: Upload individual files directly through the interface or index existing local directories on your computer without copying files.
- **Incremental Indexing & Full Rebuilds**: Detects new, modified, and deleted files within scanned directories to keep indexes current without re-indexing unchanged files. A full rebuild option is also available.
- **File Details & Document Viewing**: Inspect file previews, metadata, relevance scores, and stream or download files directly in the browser.

---

## Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | React, Vite, Tailwind CSS, Lucide React, Axios |
| **Backend API** | Python, FastAPI, Uvicorn |
| **Semantic Search** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Visual Search** | OpenCLIP (`ViT-B-32`), PyTorch, Torchvision |
| **Vector Database** | ChromaDB |
| **Metadata Database** | SQLite (WAL mode) |
| **Document Processing** | PyMuPDF (`fitz`), PyPDF, python-docx, python-pptx |
| **OCR & Image Processing** | Tesseract OCR, Pytesseract, Pillow |

---

## Project Structure

```text
personal-memory-search/
├── backend/
│   ├── api/                 # FastAPI route handlers (search, scan, upload, files, status)
│   ├── database/            # SQLite schema, connection, and database file
│   ├── indexing/            # Document parsers, custom folder scanner, incremental scan
│   ├── services/            # Embedding, CLIP, OCR, hybrid ranking, and search services
│   ├── utils/               # Path normalization, scan status, and utility helpers
│   ├── full_scan.py         # Full index rebuild runner
│   └── main.py              # FastAPI application entry point
├── data/                    # Standard storage directories
│   ├── docx/
│   ├── images/
│   ├── pdfs/
│   ├── pptx/
│   └── txts/
├── frontend/
│   ├── src/                 # React UI components, API client, and styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── tests/                   # Automated unit and integration test suite
├── requirements.txt         # Backend Python dependencies
├── run_backend.bat          # Windows backend startup batch script
└── README.md
```

---

## Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: v18 or higher, and **npm**
- **Tesseract OCR** *(optional)*: Required if you want text extracted from scanned images. If omitted, visual CLIP search still functions.

---

## Installation and Running

### 1. Clone the Repository

```bash
git clone https://github.com/SouravPaul2002/personal-memory-search.git
cd personal-memory-search
```

### 2. Set Up the Backend

Create and activate a Python virtual environment:

**On Linux / macOS:**
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv backend\venv
.\backend\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv backend\venv
backend\venv\Scripts\activate.bat
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI backend server:

```bash
python -m uvicorn backend.main:app --port 8000 --reload
```

*Windows users can alternatively run `run_backend.bat` directly from the project root.*

- **Backend API**: `http://localhost:8000`
- **Interactive API Documentation**: `http://localhost:8000/docs`

---

### 3. Set Up the Frontend

Open a new terminal window, navigate to the `frontend` directory, install packages, and start the development server:

```bash
cd frontend
npm install
npm run dev
```

*(On Windows PowerShell, if script execution policy blocks `npm`, run `npm.cmd install` and `npm.cmd run dev`.)*

- **Frontend Application**: `http://localhost:3000`

---

## Basic Usage

1. **Adding Files**:
   - **Upload**: Drop files or select documents using the upload panel to save them into standard storage.
   - **Scan a Local Folder**: Enter the absolute path to any directory on your computer (e.g. `C:\Users\Username\Documents` or `D:\Photos`) to index it directly in place.
2. **Searching**:
   - Enter queries such as `"machine learning lecture notes"`, `"invoices from last month"`, or visual queries like `"sunset on the beach"`.
   - Filter results by category (`All`, `PDF`, `Images`, `Text`, `Word`, `Presentations`).
3. **Viewing Results**:
   - Click on search results to inspect extracted text snippets, matched keywords, metadata, and preview or open files.
4. **Updating the Index**:
   - Trigger an **Incremental Scan** from the UI or API (`POST /scan/incremental`) to reconcile changes in standard folders.
   - Trigger a **Folder Scan** (`POST /scan/folder`) to detect additions, modifications, or deletions in a custom folder.
   - **Full Index Rebuild** (`POST /scan/full`): Clears the existing ChromaDB collections and SQLite file records, then re-indexes standard storage folders from scratch.

---

## Known Limitations

- **Full Index Rebuild Scope**: A full index rebuild resets the index and re-scans only standard storage folders; any custom folders must be scanned again afterwards.
- **Filename Collision in Chunks**: If two different directories contain files with the exact same file name, chunk IDs share the filename prefix in the vector index.
- **Tesseract OCR Setup**: OCR capability depends on an external Tesseract binary being installed on the system PATH or default Windows path.
- **Short Text Files**: Text files shorter than the minimum chunk threshold (100 characters) are not segmented into multi-word chunks.

---

## Repository

- **GitHub**: [https://github.com/SouravPaul2002/personal-memory-search](https://github.com/SouravPaul2002/personal-memory-search)
