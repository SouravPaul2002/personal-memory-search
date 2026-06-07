from fastapi import APIRouter

from backend.full_scan import run_full_scan
from backend.indexing.incremental_scan import (
    run_incremental_scan
)

router = APIRouter()


@router.post("/scan/incremental")
def incremental_scan():

    result = run_incremental_scan()

    return {
        "message": "Incremental scan completed",
        "result": result
    }

@router.post("/scan/full")
def full_scan():

    result = run_full_scan()

    return {
        "message": "Full scan completed",
        "result": result
    }