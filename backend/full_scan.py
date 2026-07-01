from backend.indexing.incremental_scan import (
    run_incremental_scan
)

from backend.indexing.file_registry import (
    clear_all_files
)

from backend.services.chroma_service import (
    collection,
    clip_collection
)

def run_full_scan():

    for col in [collection, clip_collection]:
        all_ids = col.get()["ids"]
        if all_ids:
            col.delete(ids=all_ids)

    clear_all_files()

    result = run_incremental_scan()

    return result