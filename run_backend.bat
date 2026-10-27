@echo off
cd /d "%~dp0"
echo Starting Personal Memory Backend on http://localhost:8000...
backend\venv\Scripts\python.exe -m uvicorn backend.main:app --port 8000 --reload
pause
