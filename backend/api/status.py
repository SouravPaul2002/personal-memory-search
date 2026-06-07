from fastapi import APIRouter

from backend.indexing.file_registry import load_registry

from backend.services.chroma_service import (
    collection
)

router = APIRouter()

chroma_documents = collection.count()

@router.get("/status")
def status():

    registry = load_registry()

    total_files = len(registry)

    pdfs = 0
    images = 0
    txts = 0
    docxs = 0
    pptxs = 0

    for data in registry.values():

        file_type = data.get(
            "file_type",
            ""
        )

        if file_type == "pdf":
            pdfs += 1

        elif file_type == "image":
            images += 1

        elif file_type == "txt":
            txts += 1

        elif file_type == "docx":
            docxs += 1

        elif file_type == "pptx":
            pptxs += 1

    return {
        "status": "running",
        "total_files": total_files,
        "indexed_chunks": chroma_documents,
        "pdfs": pdfs,
        "images": images,
        "txt": txts,
        "docx": docxs,
        "pptx": pptxs
    }