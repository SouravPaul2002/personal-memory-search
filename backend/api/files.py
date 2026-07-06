# backend/api/files.py

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # project root

router = APIRouter()

# Maps file_type to the absolute folder it lives in
FOLDER_MAP = {
    "pdf":   str(_PROJECT_ROOT / "data" / "pdfs"),
    "image": str(_PROJECT_ROOT / "data" / "images"),
    "txt":   str(_PROJECT_ROOT / "data" / "txts"),
    "docx":  str(_PROJECT_ROOT / "data" / "docx"),
    "pptx":  str(_PROJECT_ROOT / "data" / "pptx"),
}

MIME_MAP = {
    "pdf":   "application/pdf",
    "image": None,   # derived from extension
    "txt":   "text/plain",
    "docx":  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pptx":  "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

IMAGE_MIME = {
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png":  "image/png",
    ".webp": "image/webp",
}


@router.get("/files/serve/{file_type}/{file_name}")
def serve_file(file_type: str, file_name: str):
    """
    Streams a stored file back to the client.
    E.g. GET /files/serve/pdf/my-doc.pdf
    """
    folder = FOLDER_MAP.get(file_type)
    if folder is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown file_type: {file_type}"
        )

    file_path = os.path.abspath(
        os.path.join(folder, file_name)
    )

    # Safety: make sure we don't escape the data folder
    if not file_path.startswith(os.path.abspath(folder)):
        raise HTTPException(status_code=400, detail="Invalid file path")

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {file_name}"
        )

    # Determine MIME type
    mime = MIME_MAP.get(file_type)
    if mime is None:  # image — derive from extension
        ext = os.path.splitext(file_name)[1].lower()
        mime = IMAGE_MIME.get(ext, "application/octet-stream")

    return FileResponse(
        path=file_path,
        media_type=mime,
        filename=file_name
    )
