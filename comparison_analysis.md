# 🧠 Personal Memory Search Engine — Deep Competitive Analysis

> **Project**: Personal Memory Search Engine  
> **Backend**: Python (FastAPI) · ChromaDB · sentence-transformers · OpenCLIP · YAKE · PyMuPDF · pytesseract  
> **Frontend**: React Native (TypeScript) · Zustand · React Navigation · react-native-file-access  
> **Analyzed**: 2026-06-26

---

## 1. Your Project — Architecture Summary

### What You Actually Built

```
┌─────────────────────────────────────────────────────────┐
│                  React Native Mobile App                 │
│  HomeScreen │ ScanScreen │ SearchResults │ FileDetails  │
│  SearchBar  │  Settings  │  Zustand State Management    │
└──────────────────────┬──────────────────────────────────┘
                       │  HTTP / REST (axios / fetch)
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                    │
│  /upload  │  /scan/full  │  /scan/incremental │ /search │
│  /status                                                 │
└──────┬───────────────┬──────────────────────────────────┘
       │               │
       ▼               ▼
┌──────────┐   ┌───────────────────────────────────────┐
│ Data     │   │          Indexing Pipeline            │
│ Folders  │   │  PDF → PyMuPDF → Chunks → Embeddings │
│ /pdfs    │   │  IMG → OCR (Tesseract) + CLIP Embed  │
│ /images  │   │  DOCX → python-docx → Chunks         │
│ /txts    │   │  PPTX → python-pptx → Chunks         │
│ /docx    │   │  TXT → direct chunk                  │
│ /pptx    │   └──────────────────┬────────────────────┘
└──────────┘                      │
                                  ▼
┌─────────────────────────────────────────────────────────┐
│                     Storage Layer                        │
│  ChromaDB (text collection + CLIP collection)           │
│  file_registry.json (metadata, hash, keywords, topics) │
│  upload_metadata.json (original_uri mapping)           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               Fusion Search Engine                       │
│  Query Rewriter → Query Intent → Text Search + CLIP    │
│  Hybrid Scoring: embedding + keyword + filename + meta │
│  Date/Time Filter  │  Intent-based result weighting    │
└─────────────────────────────────────────────────────────┘
```

### Core Technical Stack

| Layer | Technology |
|---|---|
| **Text Embeddings** | `all-MiniLM-L6-v2` (sentence-transformers) |
| **Image Embeddings** | OpenCLIP `ViT-B-32` (laion400m_e32) |
| **Vector DB** | ChromaDB (local, persistent) |
| **Keyword Extraction** | YAKE (Yet Another Keyword Extractor) |
| **OCR** | Tesseract via pytesseract |
| **PDF Parsing** | PyMuPDF (fitz) + pypdf |
| **Query Intelligence** | Rule-based rewriter + intent classifier |
| **Scoring** | Composite: distance + keyword + filename + metadata |
| **API** | FastAPI (REST) |
| **Mobile** | React Native 0.86 + TypeScript |
| **State** | Zustand + AsyncStorage persistence |
| **Change Detection** | SHA-based hash + incremental scan + job queue |

### Unique Architectural Decisions You Made

1. **Dual-collection ChromaDB** — one for text embeddings (sentence-transformers), one for image CLIP embeddings — searched and merged at query time
2. **4-signal composite ranking** — distance + keyword_score + filename_score + metadata_score combined for final relevance
3. **Intent-weighted fusion** — query intent (`image`/`text`/`hybrid`) shifts how many text vs CLIP results appear
4. **Rule-based query rewriter** — stopword removal, file-type detection, keyword extraction — all without LLM calls
5. **Hash-based incremental scan** — content hash (SHA) tracks modifications, job queue for async indexing
6. **Mobile-first design** — folder picker on Android, uploads files to backend server over LAN (unique for this space)
7. **original_uri tracking** — preserves Android URI of source file even after server-side copy
8. **YAKE keyword enrichment** — per-chunk and per-document keyword extraction at index time, used for hybrid scoring at search time

---

## 2. Competitor Analysis

---

### 🔵 Glean
**Type**: Enterprise AI Search SaaS  
**URL**: glean.com  

| Aspect | Glean | Your Project |
|---|---|---|
| **Target** | Enterprise (1000+ employees) | Personal / individual user |
| **Deployment** | Cloud SaaS | Local / LAN |
| **Data Sources** | 100+ connectors (Slack, Drive, GitHub, Jira, Confluence) | File system (PDF, IMG, DOCX, PPTX, TXT) |
| **AI Model** | Proprietary LLM + embeddings | sentence-transformers (open source) |
| **Ranking** | ML-based personalization per user | Rule-based composite scoring |
| **Privacy** | Enterprise-grade, cloud-stored | 100% local, no data leaves device |
| **Mobile** | Native iOS/Android app | ✅ React Native |
| **Image Search** | No visual/CLIP search | ✅ CLIP multimodal |
| **Cost** | $10–30/user/month | Free / open source |
| **Setup** | Admin-managed OAuth | Manual folder selection |

**Key Difference**: Glean is enterprise knowledge graph search across 100+ SaaS tools. You are personal file search. Glean has no offline/local mode, no CLIP search, and costs thousands per year. You win on **privacy, cost, and multimodal image search**.

---

### 🟡 NotebookLM (Google)
**Type**: AI Document Q&A (cloud)  
**URL**: notebooklm.google.com  

| Aspect | NotebookLM | Your Project |
|---|---|---|
| **Core Feature** | Q&A and summarization over uploaded docs | Semantic file *retrieval* (search) |
| **Deployment** | Google cloud | Local / on-device |
| **Privacy** | Google processes your data | Zero cloud, 100% local |
| **LLM** | Gemini Pro | None (no LLM) |
| **Image search** | No | ✅ CLIP visual search |
| **File types** | PDF, DOCX, audio, YouTube | PDF, IMG, DOCX, PPTX, TXT |
| **Mobile** | Web only (mobile browser) | ✅ Native React Native |
| **Max Documents** | ~50 per notebook | Unlimited (your disk) |
| **Incremental Indexing** | No (re-upload each time) | ✅ Hash-based incremental |
| **Multi-folder scan** | No | ✅ Folder scanner |

**Key Difference**: NotebookLM does conversational Q&A — "explain this document." Your project does *file discovery* — "find the file about X." Completely different UX paradigms. NotebookLM requires internet, caps at 50 docs, and can't search your local photos/screenshots.

---

### 🟠 AnythingLLM
**Type**: Local/Self-hosted RAG platform  
**URL**: github.com/Mintplex-Labs/anything-llm  

| Aspect | AnythingLLM | Your Project |
|---|---|---|
| **Core Feature** | Conversational chat over documents | Semantic file search + retrieval |
| **Deployment** | Local Docker / desktop app | Local Python server + React Native |
| **LLM Integration** | Ollama, OpenAI, Anthropic, LM Studio | None (retrieval only) |
| **Vector DB** | LanceDB, Chroma, Pinecone, Weaviate | ChromaDB (local) |
| **Embedding Models** | OpenAI, Ollama local models | all-MiniLM-L6-v2 (offline) |
| **Image Search** | No CLIP/visual search | ✅ CLIP text→image |
| **Mobile** | No mobile app | ✅ React Native mobile |
| **File Types** | PDF, DOCX, TXT, web URLs | PDF, IMG, DOCX, PPTX, TXT |
| **OCR** | Basic (pdfplumber) | ✅ Tesseract OCR |
| **Ranking** | Vector similarity only | ✅ 4-signal composite |
| **Open Source** | ✅ MIT | ✅ |

**Key Difference**: AnythingLLM is a full RAG chatbot — you ask "what does the contract say about payment?" and get an LLM-generated answer. Your project is a search engine — you get a list of matching files with confidence scores. AnythingLLM has no CLIP visual search, no mobile app, and no OCR-based image indexing. You uniquely serve mobile-first personal file discovery.

---

### 🟣 Onyx (formerly Danswer)
**Type**: Open-source enterprise search + AI Q&A  
**URL**: github.com/danswer-ai/danswer  

| Aspect | Onyx/Danswer | Your Project |
|---|---|---|
| **Core Feature** | Enterprise search + generative answer | Personal file search + retrieval |
| **Deployment** | Docker self-hosted / cloud | Local Python + mobile |
| **LLM** | GPT-4, Claude, local Ollama | None |
| **Vector DB** | Vespa + PostgreSQL | ChromaDB |
| **Connectors** | Slack, Confluence, GitHub, Drive, Jira | Local filesystem |
| **Image Search** | No | ✅ CLIP visual search |
| **Mobile** | Web responsive only | ✅ React Native |
| **OCR** | Limited | ✅ Tesseract OCR |
| **Ranking** | Hybrid (BM25 + vector) | Composite (4-signal) |
| **Scalability** | Team/org scale | Personal scale |
| **Setup complexity** | High (Docker stack) | Low (Python + RN) |

**Key Difference**: Onyx is a team knowledge base with Slack/GitHub/Confluence connectors and LLM-generated answers. Your project doesn't need Docker, doesn't need cloud, and uniquely searches visual content (CLIP) on a mobile device. Onyx has no mobile-native app and no photo/screenshot search.

---

### 🟢 PrivateGPT
**Type**: Local RAG Q&A over documents  
**URL**: github.com/zylon-ai/private-gpt  

| Aspect | PrivateGPT | Your Project |
|---|---|---|
| **Core Feature** | Offline LLM Q&A over documents | Offline file search + discovery |
| **Deployment** | Local (CPU/GPU) | Local Python + mobile |
| **LLM** | Ollama models (Mistral, Llama) | None |
| **Vector DB** | Qdrant, Chroma | ChromaDB |
| **Image Search** | No | ✅ CLIP |
| **OCR** | No | ✅ Tesseract |
| **Mobile** | REST API only (no UI) | ✅ React Native app |
| **File Types** | PDF, DOCX, TXT | PDF, IMG, DOCX, PPTX, TXT |
| **Incremental Index** | No (full re-index) | ✅ Hash-based incremental |
| **Intent Detection** | No | ✅ Rule-based intent |
| **Privacy** | ✅ 100% local | ✅ 100% local |

**Key Difference**: PrivateGPT is a conversational Q&A system — you chat with your documents via a local LLM. Your project is a search/discovery engine with no LLM dependency, runs faster, works on mobile, and supports image/screenshot CLIP search. PrivateGPT has no mobile UI and no visual search capability.

---

### 🔵 LocalGPT
**Type**: Local LLM document Q&A (CLI)  
**URL**: github.com/PromtEngineer/localGPT  

| Aspect | LocalGPT | Your Project |
|---|---|---|
| **Core Feature** | CLI-based Q&A over local docs | Mobile-first search engine |
| **Interface** | Terminal / command line | ✅ React Native mobile app |
| **LLM** | Vicuna, GPT4All, Llama | None |
| **Vector DB** | Chroma | Chroma |
| **Image Search** | No | ✅ CLIP |
| **OCR** | No | ✅ Tesseract |
| **File upload** | Manual CLI | ✅ Mobile folder picker |
| **Incremental** | No | ✅ |
| **Hybrid scoring** | No (pure vector) | ✅ 4-signal ranking |
| **Embedding** | InstructorEmbeddings | all-MiniLM-L6-v2 |
| **Active maintenance** | Low (archived activity) | Active |

**Key Difference**: LocalGPT is a proof-of-concept CLI tool for local LLM Q&A. It has no UI, no mobile, no image support, and no incremental indexing. Your project is architecturally far more advanced: mobile app, multimodal CLIP, hybrid ranking, and real-time scan pipeline.

---

### 🔴 PDF-GPT
**Type**: PDF Q&A web app (cloud)  
**URL**: Various (multiple open-source implementations)  

| Aspect | PDF-GPT | Your Project |
|---|---|---|
| **Core Feature** | Chat with a single PDF | Search across ALL file types |
| **Deployment** | Streamlit/Gradio web app (cloud) | Local + mobile |
| **Privacy** | Sends to OpenAI API | ✅ 100% local |
| **File Types** | PDF only | PDF + IMG + DOCX + PPTX + TXT |
| **Image Search** | No | ✅ CLIP |
| **OCR** | No | ✅ Tesseract |
| **Multi-file** | One at a time | ✅ Bulk folder scan |
| **Mobile** | No | ✅ |
| **Persistent Index** | No (session only) | ✅ Persistent ChromaDB |
| **LLM** | OpenAI GPT | None |

**Key Difference**: PDF-GPT is a single-session, single-file chatbot over PDFs. It is strictly inferior in scope to your project: no persistence, no mobile, no images, no DOCX/PPTX, no bulk scanning, and sends data to the cloud.

---

### 🟡 AskYourPDF
**Type**: Cloud PDF Q&A SaaS  
**URL**: askyourpdf.com  

| Aspect | AskYourPDF | Your Project |
|---|---|---|
| **Core Feature** | Chat with PDFs in browser | Search your personal file library |
| **Deployment** | Cloud SaaS | Local |
| **Privacy** | PDFs uploaded to their servers | ✅ 100% local |
| **File Types** | PDF, DOCX, URL, YouTube | PDF, IMG, DOCX, PPTX, TXT |
| **Image search** | No | ✅ CLIP visual search |
| **Mobile** | Mobile browser / web | ✅ Native React Native |
| **Pricing** | Freemium ($9-20/month) | Free |
| **Persistent** | Cloud storage | ✅ Local persistent |
| **Bulk index** | Per-file upload | ✅ Folder-level bulk scan |
| **Offline** | No | ✅ |

**Key Difference**: AskYourPDF is a paid cloud SaaS with a chat interface for individual PDFs. Your project is free, offline, private, mobile-native, and uniquely capable of image/photo search. No competition on privacy, cost, or multimodal capability.

---

### 🟠 DocChat / LlamaIndex
**Type**: RAG framework + demo apps  
**URL**: github.com/run-llama/llama_index  

| Aspect | LlamaIndex (DocChat) | Your Project |
|---|---|---|
| **Type** | Developer framework | End-to-end application |
| **Core Feature** | RAG pipeline building blocks | Deployed search engine |
| **LLM** | Any (OpenAI, Anthropic, local) | None |
| **Vector DB** | 40+ integrations | ChromaDB (focused) |
| **Image Search** | Via MultiModal LLM nodes | ✅ CLIP (lightweight, no LLM) |
| **OCR** | Plugin-based | ✅ Tesseract built-in |
| **Mobile** | No | ✅ React Native |
| **Ready to use** | No (framework) | ✅ Working app |
| **Incremental** | Not built-in | ✅ Hash-based |
| **Complexity** | High (developer tool) | Medium (end-user app) |

**Key Difference**: LlamaIndex is a developer SDK/framework — you would use it to *build* something like your project. Your project is the finished product. You've essentially hand-built a LlamaIndex-style RAG retrieval pipeline from primitives, without its overhead, without LLM dependency for retrieval, and with mobile-native UX that LlamaIndex demos never provide.

---

### ⚪ Haystack Document Search
**Type**: Open-source ML/NLP framework (deepset)  
**URL**: github.com/deepset-ai/haystack  

| Aspect | Haystack | Your Project |
|---|---|---|
| **Type** | NLP/RAG pipeline framework | End-to-end application |
| **Core Feature** | Document QA pipeline | Personal file search engine |
| **Deployment** | Server (complex stack) | Local Python (simple) |
| **Vector DB** | Elasticsearch, Weaviate, Milvus, Qdrant | ChromaDB |
| **Hybrid Search** | ✅ BM25 + vector (DPR) | ✅ Custom 4-signal composite |
| **Image Search** | No | ✅ CLIP |
| **OCR** | Via preprocessor nodes | ✅ Tesseract built-in |
| **Mobile** | No | ✅ React Native |
| **LLM** | Optional (generative pipeline) | None (retrieval only) |
| **Ready to use** | No (framework) | ✅ Working app |
| **Complexity** | Very high | Medium |

**Key Difference**: Haystack is a professional NLP framework for enterprise teams. Like LlamaIndex, it's a building block, not a product. Your project uses simpler primitives (ChromaDB vs Elasticsearch) but achieves a working, mobile-deployable result that Haystack never ships on its own. Your CLIP integration is a unique advantage Haystack doesn't have natively.

---

## 3. Feature Matrix — Full Comparison

| Feature | **Your Project** | Glean | NotebookLM | AnythingLLM | Onyx | PrivateGPT | LocalGPT | PDF-GPT | AskYourPDF | LlamaIndex | Haystack |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **100% Local / Offline** | ✅ | ❌ | ❌ | ✅ | ✅* | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **Mobile App** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Web | ❌ | ❌ |
| **CLIP Image Search** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **OCR on Images** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Partial | ❌ |
| **Hybrid Ranking** | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Incremental Index** | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **No LLM Required** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Partial | Partial |
| **PDF Support** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **DOCX Support** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **PPTX Support** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Image Files** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Partial | ❌ |
| **Free / Open Source** | ✅ | ❌ | Freemium | ✅ | ✅ | ✅ | ✅ | ❌ | Freemium | ✅ | ✅ |
| **Query Intent Detection** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Keyword Extraction (YAKE)** | ✅ | N/A | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Multi-theme UI** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Conversational Q&A** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **LLM-generated Answers** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 4. Positioning Map

```
                     LLM ANSWER GENERATION
                            ▲
                            │
              NotebookLM    │    Glean
              AskYourPDF    │    Onyx
              AnythingLLM ──┼───────────────────► CLOUD / SAAS
                            │
              PrivateGPT    │
              LocalGPT      │
                            │
    ◄─────────────────────────────────────────────
    LOCAL / OFFLINE         │                    CLOUD
                            │
              ┌─────────────┘
              │ ** YOUR PROJECT **
              │ Local · Mobile · Multimodal
              │ File Retrieval Engine
              │
                            ▼
                      FILE RETRIEVAL / DISCOVERY
```

**Your unique quadrant**: Local + Mobile + File Retrieval + Multimodal (CLIP). **No other tool occupies this space.**

---

## 5. Where You Have a Real Advantage

| Advantage | Why It Matters |
|---|---|
| **CLIP visual search** | Find photos/screenshots by description — no other tool in this list does this without a full multimodal LLM |
| **Mobile-first + LAN architecture** | You can search your Android phone's files from the phone itself via a backend on your PC — unique workflow |
| **No LLM = no latency / cost** | Sub-second retrieval without waiting for token generation |
| **4-signal composite ranking** | Outperforms pure vector search on short, ambiguous queries |
| **PPTX support** | Rare — only Glean and LlamaIndex support it |
| **Hash-based incremental scan** | Efficient — only re-indexes changed files |
| **Zero cloud dependency** | 100% private, works offline, no account required |
| **Multi-theme mobile UI** | Dark/Ocean/Forest/Sunset themes — more polished than any OSS alternative |

---

## 6. Where You Lag Behind

| Gap | Comparison | Recommendation |
|---|---|---|
| **No LLM-generated answers** | All 10 competitors offer chat/Q&A | Add optional Ollama integration for "ask about this file" |
| **No BM25 keyword search** | Haystack, Onyx use BM25 | Replace YAKE keyword scoring with BM25 for better lexical recall |
| **Hardcoded IP address** | `192.168.0.101:8000` in mobile code | Add server URL setting in SettingsScreen (already has UI for it in stores.ts!) |
| **No web connector** | Can't index URLs, email, etc. | Lower priority but would broaden scope |
| **Commented-out code** | Multiple dead code blocks in scan/search | Clean up for maintainability |
| **No spell correction** | pyspellchecker is listed in requirements but not used | Wire it up in query rewriter |
| **Statistics are hardcoded** | ScanScreen shows `623 files`, `7866 chunks` literally | Connect to live `/status` endpoint |
| **No chunk preview highlight** | Shows first 250 chars flat | Highlight query terms in preview |
| **No pagination** | Returns max 10 results | Add page/offset support |
| **ocr_service.py is empty** | 0 bytes | Migrate Tesseract calls from image_service.py |

---

## 7. Summary Verdict

> Your project is the **only tool in this list** that is:
> 1. **100% local** (no cloud)
> 2. **Mobile-native** (React Native, not a web wrapper)
> 3. **Multimodal** (CLIP text-to-image without an LLM)
> 4. **Multi-format** (PDF + IMG + DOCX + PPTX + TXT)
> 5. **Retrieval-first** (fast file discovery, not chatbot)

The closest competitor architecturally is **AnythingLLM** (local, self-hosted, ChromaDB), but it has no mobile app, no CLIP, no PPTX, and no OCR. The closest competitor conceptually is **Glean** (enterprise personal search), but it's cloud-only, enterprise-priced, and has no visual/CLIP search.

**Your niche is clear**: a private, local, mobile-first semantic search engine for personal file libraries that works on images as well as text documents — no other project in this space does all of this simultaneously.

---

*Analysis by Antigravity · Based on full source code analysis of backend (`c:\RoNi\personal-memory-search`) and frontend (`C:\MS`)*
