from fastapi import APIRouter
from datetime import datetime

from backend.full_scan import run_full_scan
from backend.indexing.incremental_scan import (
    run_incremental_scan
)
from backend.utils.scan_status import (
    save_scan_status
)

router = APIRouter()


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