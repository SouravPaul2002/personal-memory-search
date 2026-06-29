# backend/api/upload.py

from fastapi import APIRouter, UploadFile, File,  Form
import os
import json

from backend.indexing.incremental_scan import run_incremental_scan

router = APIRouter()

def get_save_folder(filename: str):

    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        return "data/pdfs"

    elif ext in ["jpg", "jpeg", "png", "webp"]:
        return "data/images"

    elif ext == "txt":
        return "data/txts"

    elif ext == "docx":
        return "data/docx"

    elif ext == "pptx":
        return "data/pptx"

    return None

UPLOAD_DIR = "data/pdfs"

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

    # --- Write to upload_metadata.json (used by incremental scan for new files) ---
    metadata_file = (
        "data/upload_metadata.json"
    )

    if os.path.exists(metadata_file):

        try:

            with open(
                metadata_file,
                "r",
                encoding="utf-8"
            ) as f:

                metadata = json.load(f)

        except Exception:

            metadata = {}

    else:

        metadata = {}


    metadata[file.filename] = {
        "original_uri": original_uri
    }

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    # run_incremental_scan()

    return {
        "success": True,
        "filename": file.filename
    }