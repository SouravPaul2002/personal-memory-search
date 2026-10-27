# Personal Memory Search — Web Frontend

A clean React (Vite) web application interface for the Personal Memory Search Engine. Connects directly to the local FastAPI backend running on port 8000.

## 📁 Folder Structure

```
frontend/
├── public/                 # Static public assets
├── src/
│   ├── assets/             # Images, icons, SVGs
│   ├── components/
│   │   ├── common/         # Buttons, badges, spinners, modals
│   │   ├── layout/         # Header, Navbar, Sidebar, Footer
│   │   ├── search/         # SearchBar, FilterChips, ResultCards
│   │   └── upload/         # Drag-and-drop file upload modals
│   ├── context/            # React Context or global state
│   ├── hooks/              # Custom hooks (e.g., useDebounce, useSearch)
│   ├── pages/              # Top-level route pages (Home, Results, Dashboard)
│   ├── services/
│   │   └── api.js          # Pre-configured Axios service for FastAPI endpoints
│   ├── utils/              # Helper utilities (formatters, date parsers)
│   ├── App.jsx             # Main root component
│   ├── main.jsx            # Application mount point
│   └── index.css           # Global CSS variables & reset styles
├── .env.example            # Environment variables template
├── .gitignore              # Git ignored files (node_modules, build, etc.)
├── index.html              # HTML5 entry template
├── package.json            # Scripts & dependencies
└── vite.config.js          # Vite config with backend proxy to localhost:8000
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development Server
```bash
npm run dev
```
The app will run on `http://localhost:3000`.

### 3. Connect to FastAPI Backend
Ensure your FastAPI backend is running:
```bash
cd ..
uvicorn backend.main:app --reload
```
API requests to `/api/*` in Vite will automatically proxy to `http://localhost:8000`.
