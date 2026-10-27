from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os

from backend.full_scan import run_full_scan
from backend.indexing.incremental_scan import (
    run_incremental_scan
)
from backend.indexing.folder_scanner import (
    scan_custom_folder
)
from backend.utils.scan_status import (
    save_scan_status
)

router = APIRouter()


class FolderScanRequest(BaseModel):
    folder_path: str
    recursive: bool = True


@router.post("/scan/incremental")
def incremental_scan():

    result = run_incremental_scan()

    save_scan_status(
        last_scan_time=datetime.now().isoformat(),
        last_scan_type="incremental"
    )

    return {
        "message": "Incremental scan completed",
        "new_files": result["new_files"],
        "modified_files": result["modified_files"],
        "deleted_files": result["deleted_files"]
    }


@router.post("/scan/full")
def full_scan():

    result = run_full_scan()

    save_scan_status(
        last_scan_time=datetime.now().isoformat(),
        last_scan_type="full"
    )

    return {
        "message": "Full scan completed",
        "new_files": result["new_files"],
        "modified_files": result["modified_files"],
        "deleted_files": result["deleted_files"]
    }


@router.post("/scan/folder")
def scan_folder(req: FolderScanRequest):
    """
    Scans a local directory on the server/machine and indexes all supported
    images and documents directly without requiring one-by-one file uploads.
    """
    if not req.folder_path or not req.folder_path.strip():
        raise HTTPException(status_code=400, detail="Folder path cannot be empty")

    try:
        result = scan_custom_folder(req.folder_path, recursive=req.recursive)
        
        save_scan_status(
            last_scan_time=datetime.now().isoformat(),
            last_scan_type=f"folder ({os.path.basename(result['folder']) or result['folder']})"
        )

        return {
            "success": True,
            "message": f"Folder scan complete: {result['new_files']} added, {result['modified_files']} updated, {result['skipped_files']} unchanged.",
            **result
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Folder scan failed: {str(e)}")