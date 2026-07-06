# backend/api/upload.py

from fastapi import APIRouter, UploadFile, File,  Form
import os
import json
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # project root

from backend.indexing.incremental_scan import run_incremental_scan

router = APIRouter()

def get_save_folder(filename: str):

    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        return str(_PROJECT_ROOT / "data" / "pdfs")

    elif ext in ["jpg", "jpeg", "png", "webp"]:
        return str(_PROJECT_ROOT / "data" / "images")

    elif ext == "txt":
        return str(_PROJECT_ROOT / "data" / "txts")

    elif ext == "docx":
        return str(_PROJECT_ROOT / "data" / "docx")

    elif ext == "pptx":
        return str(_PROJECT_ROOT / "data" / "pptx")

    return None

UPLOAD_DIR = str(_PROJECT_ROOT / "data" / "pdfs")

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    original_uri: str = Form(...)
):
    
    print("==========")
    print("FILE:", file.filename)
    print("URI:", original_uri)
    print("==========")

    folder = get_save_folder(
        file.filename
    )

    if folder is None:
        return {
            "success": False,
            "message": "Unsupported file type"
        }

    os.makedirs(
        folder,
        exist_ok=True
    )

    save_path = os.path.join(
        folder,
        file.filename
    )

    with open(
        save_path,
        "wb"
    ) as f:

        content = await file.read()
        f.write(content)

    # --- Write upload metadata to SQLite database ---
    from backend.indexing.file_registry import save_upload_metadata
    save_upload_metadata(file.filename, original_uri)

    # run_incremental_scan()

    return {
        "success": True,
        "filename": file.filename
    }