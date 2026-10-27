import os
import time
from pathlib import Path

from backend.indexing.file_registry import (
    get_all_files,
    insert_file,
    update_file,
)
from backend.services.file_metadata_service import get_mime_type
from backend.services.hash_service import get_file_hash

from backend.indexing.pdf_indexer import index_pdf, delete_pdf_chunks
from backend.indexing.image_indexer import index_image, delete_image_chunks
from backend.indexing.txt_indexer import index_txt, delete_txt_chunks
from backend.indexing.docx_indexer import index_docx, delete_docx_chunks
from backend.indexing.pptx_indexer import index_pptx, delete_pptx_chunks

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
DOCX_EXTS = {".docx"}
PPTX_EXTS = {".pptx"}
PDF_EXTS = {".pdf"}
TXT_EXTS = {".txt", ".md"}

SUPPORTED_EXTS = IMAGE_EXTS | DOCX_EXTS | PPTX_EXTS | PDF_EXTS | TXT_EXTS


_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def scan_custom_folder(folder_path: str, recursive: bool = True):
    """
    Scans a user-specified folder on the local machine and indexes all
    supported images, PDFs, text files, Word documents, and PowerPoint decks.
    Supports both absolute paths (e.g. D:\Photos) and relative paths (e.g. data/images).
    """
    raw_path = folder_path.strip().strip('"').strip("'")
    if not os.path.isabs(raw_path):
        clean_folder = os.path.abspath(os.path.join(_PROJECT_ROOT, raw_path))
    else:
        clean_folder = os.path.abspath(raw_path)

    if not os.path.exists(clean_folder):
        raise ValueError(f"Folder path does not exist: {clean_folder}")

    if not os.path.isdir(clean_folder):
        raise ValueError(f"Path is not a directory: {clean_folder}")

    # Load existing registry as dicts
    db_files = get_all_files()
    registry = {row["file_uri"]: dict(row) for row in db_files}

    new_files = 0
    modified_files = 0
    skipped_files = 0
    errors = []
    total_found = 0

    # Discover files
    collected_paths = []
    if recursive:
        for root, _, files in os.walk(clean_folder):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTS:
                    collected_paths.append(os.path.join(root, file))
    else:
        for file in os.listdir(clean_folder):
            full_p = os.path.join(clean_folder, file)
            if os.path.isfile(full_p):
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTS:
                    collected_paths.append(full_p)

    total_found = len(collected_paths)

    for full_path in collected_paths:
        abs_path = os.path.abspath(full_path)
        filename = os.path.basename(abs_path)
        ext = os.path.splitext(filename)[1].lower()

        try:
            file_hash = get_file_hash(abs_path)
            stat = os.stat(abs_path)
            file_size = stat.st_size
            created_time = datetime_from_timestamp(stat.st_ctime)
            modified_time = datetime_from_timestamp(stat.st_mtime)
            mime_type = get_mime_type(abs_path)

            # Determine file category
            if ext in IMAGE_EXTS:
                file_type = "image"
            elif ext in PDF_EXTS:
                file_type = "pdf"
            elif ext in TXT_EXTS:
                file_type = "txt"
            elif ext in DOCX_EXTS:
                file_type = "docx"
            elif ext in PPTX_EXTS:
                file_type = "pptx"
            else:
                continue

            # Check if unchanged
            if abs_path in registry and registry[abs_path].get("content_hash") == file_hash:
                skipped_files += 1
                continue

            # If modified, remove old chunks first
            is_modified = abs_path in registry
            if is_modified:
                _delete_chunks_for_file(file_type, filename)

            # Index based on type
            result = None
            if file_type == "image":
                result = index_image(abs_path, filename)
            elif file_type == "pdf":
                result = index_pdf(abs_path, filename)
            elif file_type == "txt":
                result = index_txt(abs_path, filename)
            elif file_type == "docx":
                result = index_docx(abs_path, filename)
            elif file_type == "pptx":
                result = index_pptx(abs_path, filename)

            if not result:
                result = {"keywords": [], "topics": [], "summary": ""}

            # Upsert into database
            if is_modified:
                update_file(
                    file_uri=abs_path,
                    original_uri=abs_path,
                    file_name=filename,
                    file_type=file_type,
                    mime_type=mime_type,
                    file_size=file_size,
                    modified_time=modified_time,
                    content_hash=file_hash,
                    keywords=result.get("keywords", []),
                    topics=result.get("topics", []),
                    summary=result.get("summary", "")
                )
                modified_files += 1
            else:
                insert_file(
                    file_uri=abs_path,
                    original_uri=abs_path,
                    file_name=filename,
                    file_type=file_type,
                    mime_type=mime_type,
                    file_size=file_size,
                    created_time=created_time,
                    modified_time=modified_time,
                    last_access_time=time.time(),
                    content_hash=file_hash,
                    keywords=result.get("keywords", []),
                    topics=result.get("topics", []),
                    summary=result.get("summary", "")
                )
                new_files += 1

        except Exception as e:
            errors.append(f"{filename}: {str(e)}")

    return {
        "folder": clean_folder,
        "total_scanned": total_found,
        "new_files": new_files,
        "modified_files": modified_files,
        "skipped_files": skipped_files,
        "errors": errors[:10]  # Return up to 10 error snippets
    }


def _delete_chunks_for_file(file_type: str, filename: str):
    try:
        if file_type == "pdf":
            delete_pdf_chunks(filename)
        elif file_type == "image":
            delete_image_chunks(filename)
        elif file_type == "txt":
            delete_txt_chunks(filename)
        elif file_type == "docx":
            delete_docx_chunks(filename)
        elif file_type == "pptx":
            delete_pptx_chunks(filename)
    except Exception as e:
        print(f"Error deleting chunks for {filename}: {e}")


def datetime_from_timestamp(ts):
    from datetime import datetime
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)
