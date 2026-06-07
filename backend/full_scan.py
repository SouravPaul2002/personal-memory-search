from backend.indexing.incremental_scan import (
    run_incremental_scan
)

from backend.indexing.file_registry import (
    save_registry
)

from backend.services.chroma_service import (
    collection
)

def run_full_scan():

    all_ids = collection.get()["ids"]

    if all_ids:
        collection.delete(ids=all_ids)

    save_registry({})

    result = run_incremental_scan()

    return result