from fastapi import APIRouter

from backend.database.database import get_connection

from backend.services.chroma_service import (
    collection
)
from backend.utils.scan_status import (
    load_scan_status
)

router = APIRouter()


@router.get("/status")
def status():

    conn = get_connection()
    cursor = conn.cursor()
    
    # Query file counts grouped by file_type
    cursor.execute(
        """
        SELECT file_type, COUNT(*) as count
        FROM files
        WHERE is_deleted = 0
        GROUP BY file_type
        """
    )
    rows = cursor.fetchall()
    
    # Total active files
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM files
        WHERE is_deleted = 0
        """
    )
    total_files = cursor.fetchone()[0]
    conn.close()

    counts = {row["file_type"]: row["count"] for row in rows}
    
    pdfs = counts.get("pdf", 0)
    images = counts.get("image", 0)
    txts = counts.get("txt", 0)
    docxs = counts.get("docx", 0)
    pptxs = counts.get("pptx", 0)

    chroma_documents = collection.count()
    scan_status = load_scan_status()

    return {
        "status": "running",
        "total_files": total_files,
        "indexed_chunks": chroma_documents,

        "pdfs": pdfs,
        "images": images,
        "txt": txts,
        "docx": docxs,
        "pptx": pptxs,

        "indexed_pdfs": pdfs,

        "indexed_images": images,

        "indexed_documents":
            txts +
            docxs +
            pptxs,

        "last_scan_time":
            scan_status.get(
                "last_scan_time"
            ),

        "last_scan_type":
            scan_status.get(
                "last_scan_type"
            )
    }