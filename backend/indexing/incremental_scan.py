import json
import os
from datetime import datetime

from backend.indexing.file_registry import (
    load_registry,
    save_registry
)

from backend.services.file_metadata_service import get_mime_type
from backend.services.hash_service import (
    get_file_hash
)

from backend.indexing.pdf_indexer import (
    index_pdf,
    delete_pdf_chunks
)

from backend.indexing.image_indexer import (
    index_image,
    delete_image_chunks
)

from backend.indexing.txt_indexer import (
    index_txt,
    delete_txt_chunks
)

from backend.indexing.docx_indexer import (
    index_docx,
    delete_docx_chunks
)

from backend.indexing.pptx_indexer import (
    index_pptx,
    delete_pptx_chunks
)

from backend.indexing.job_queue import (
    index_queue
)

from backend.indexing.worker import (
    process_jobs
)

def load_upload_metadata():

    metadata_file = (
        "data/upload_metadata.json"
    )

    if not os.path.exists(
        metadata_file
    ):
        return {}

    with open(
        metadata_file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

PDF_FOLDER = "data/pdfs"

IMAGE_FOLDER = "data/images"
IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
)

TXT_FOLDER = "data/txts"

DOCX_FOLDER = "data/docx"
DOCX_EXTENSIONS = (
    ".docx",
)

PPTX_FOLDER = "data/pptx"
PPTX_EXTENSIONS = (
    ".pptx",
)

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(TXT_FOLDER, exist_ok=True)
os.makedirs(DOCX_FOLDER, exist_ok=True)
os.makedirs(PPTX_FOLDER, exist_ok=True)

def run_incremental_scan():
    new_files = 0
    modified_files = 0
    deleted_files = 0
    registry = load_registry()

    current_files = set()

    #incremental scan for PDFS
    for filename in os.listdir(PDF_FOLDER):

        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.abspath(
            os.path.join(PDF_FOLDER, filename)
        )

        current_files.add(pdf_path)

        created_time = os.path.getctime(pdf_path)

        modified_time = os.path.getmtime(pdf_path)

        mime_type = get_mime_type(pdf_path)

        file_size = os.path.getsize(pdf_path)

        file_hash = get_file_hash(pdf_path)

        # NEW FILE
        if pdf_path not in registry:

            print(f"\nNEW PDF: {filename}")
            new_files +=1

            # result = index_pdf(
            #     pdf_path=pdf_path,
            #     filename=filename
            # )
            index_queue.put(
                {
                    "type": "pdf",
                    "action": "new",
                    "pdf_path": pdf_path,
                    "filename": filename,
                    "created_time": created_time,
                    "modified_time": modified_time,
                    "mime_type": mime_type,
                    "file_size": file_size,
                    "file_hash": file_hash
                }
            )

            # if result is None:
            #     continue

            # registry[pdf_path] = {
            #     "file_name": filename,
            #     "file_type": "pdf",
            #     "created_time": created_time,
            #     "modified_time": modified_time,
            #     "mime_type": mime_type,
            #     "file_size": file_size,
            #     "content_hash": file_hash,
            #     "keywords": result["keywords"],
            #     "last_indexed": datetime.now().isoformat()
            # }

        # MODIFIED FILE
        elif registry[pdf_path]["content_hash"] != file_hash:

            print(f"\nMODIFIED PDF: {filename}")
            modified_files +=1

            # delete_pdf_chunks(filename)

            # result= index_pdf(
            #     pdf_path=pdf_path,
            #     filename=filename
            # )

            # registry[pdf_path]["modified_time"] = modified_time
            # registry[pdf_path]["mime_type"] = mime_type
            # registry[pdf_path]["file_size"] = file_size
            # registry[pdf_path]["content_hash"] = file_hash
            # registry[pdf_path]["last_indexed"] = datetime.now().isoformat()
            # registry[pdf_path]["keywords"] = result["keywords"]

    # incremental scan for Images
    for filename in os.listdir(IMAGE_FOLDER):

        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue

        image_path = os.path.abspath(
            os.path.join(IMAGE_FOLDER, filename)
        )

        current_files.add(image_path)

        modified_time = os.path.getmtime(image_path)

        created_time = os.path.getctime(image_path)

        mime_type = get_mime_type(
            image_path
        )

        file_size = os.path.getsize(image_path)

        file_hash = get_file_hash(image_path)

        # NEW FILE
        if image_path not in registry:

            print(f"\nNEW IMAGE: {filename}")
            new_files +=1

            # result = index_image(
            #     image_path=image_path,
            #     filename=filename
            # )

            # if result is None:
            #     continue

            # registry[image_path] = {
            #     "file_name": filename,
            #     "file_type": "image",
            #     "created_time": created_time,
            #     "modified_time": modified_time,
            #     "mime_type": mime_type,
            #     "file_size": file_size,
            #     "content_hash": file_hash,
            #     "keywords": result["keywords"],
            #     "last_indexed": datetime.now().isoformat()
            # }
            index_queue.put(
                {
                    "type": "image",
                    "action": "new",
                    "image_path": image_path,
                    "filename": filename,
                    "created_time": created_time,
                    "modified_time": modified_time, 
                    "mime_type": mime_type,
                    "file_size": file_size,
                    "file_hash": file_hash
                }
            )

        # MODIFIED FILE
        elif registry[image_path]["content_hash"] != file_hash:

            print(f"\nMODIFIED IMAGE: {filename}")
            modified_files +=1

            delete_image_chunks(filename)

            result = index_image(
                image_path=image_path,
                filename=filename
            )

            if result is None:
                continue

            registry[image_path]["modified_time"] = modified_time
            registry[image_path]["mime_type"] = mime_type
            registry[image_path]["file_size"] = file_size
            registry[image_path]["content_hash"] = file_hash
            registry[image_path]["last_indexed"] = datetime.now().isoformat()
            registry[image_path]["keywords"] = result["keywords"]

    #incremental scan for TXT
    for filename in os.listdir(TXT_FOLDER):

        if not filename.lower().endswith(".txt"):
            continue

        txt_path = os.path.abspath(
            os.path.join(TXT_FOLDER, filename)
        )

        current_files.add(txt_path)

        modified_time = os.path.getmtime(txt_path)

        created_time = os.path.getctime(txt_path)

        mime_type = get_mime_type(
            txt_path
        )

        file_size = os.path.getsize(txt_path)

        file_hash = get_file_hash(txt_path)

        # NEW FILE
        if txt_path not in registry:

            print(f"\nNEW TXT: {filename}")
            new_files +=1

            result = index_txt(
                txt_path=txt_path,
                filename=filename
            )

            if result is None:
                continue

            registry[txt_path] = {
                "file_name": filename,
                "file_type": "txt",
                "created_time": created_time,
                "modified_time": modified_time,
                "mime_type": mime_type,
                "file_size": file_size,
                "content_hash": file_hash,
                "keywords": result["keywords"],
                "topics": result["topics"],
                "summary": result["summary"],
                "last_indexed": datetime.now().isoformat()
            }

        # MODIFIED FILE
        elif registry[txt_path]["content_hash"] != file_hash:

            print(f"\nMODIFIED TXT: {filename}")
            modified_files +=1

            delete_txt_chunks(filename)

            result= index_txt(
                txt_path=txt_path,
                filename=filename
            )

            registry[txt_path]["modified_time"] = modified_time
            registry[txt_path]["mime_type"] = mime_type
            registry[txt_path]["file_size"] = file_size
            registry[txt_path]["content_hash"] = file_hash
            registry[txt_path]["last_indexed"] = datetime.now().isoformat()
            registry[txt_path]["keywords"] = result["keywords"]

    #incremental scan for DOCX
    for filename in os.listdir(DOCX_FOLDER):

        if not filename.lower().endswith(DOCX_EXTENSIONS):
            continue

        docx_path = os.path.abspath(
            os.path.join(DOCX_FOLDER, filename)
        )

        current_files.add(docx_path)

        modified_time = os.path.getmtime(docx_path)

        created_time = os.path.getctime(docx_path)

        mime_type = get_mime_type(
            docx_path
        )

        file_size = os.path.getsize(docx_path)

        file_hash = get_file_hash(docx_path)

        # NEW FILE
        if docx_path not in registry:

            print(f"\nNEW DOCX: {filename}")
            new_files +=1

            result = index_docx(
                docx_path=docx_path,
                filename=filename
            )

            if result is None:
                continue

            registry[docx_path] = {
                "file_name": filename,
                "file_type": "docx",
                "created_time": created_time,
                "modified_time": modified_time,
                "mime_type": mime_type,
                "file_size": file_size,
                "content_hash": file_hash,
                "keywords": result["keywords"],
                "topics": result["topics"],
                "summary": result["summary"],
                "last_indexed": datetime.now().isoformat()
            }

        # MODIFIED FILE
        elif registry[docx_path]["content_hash"] != file_hash:

            print(f"\nMODIFIED DOCX: {filename}")
            modified_files +=1

            delete_docx_chunks(filename)

            result= index_docx(
                docx_path=docx_path,
                filename=filename
            )

            registry[docx_path]["modified_time"] = modified_time
            registry[docx_path]["mime_type"] = mime_type
            registry[docx_path]["file_size"] = file_size
            registry[docx_path]["content_hash"] = file_hash
            registry[docx_path]["last_indexed"] = datetime.now().isoformat()
            registry[docx_path]["keywords"] = result["keywords"]


    #incremental scan for PPTX
    for filename in os.listdir(PPTX_FOLDER):

        if not filename.lower().endswith(PPTX_EXTENSIONS):
            continue

        pptx_path = os.path.abspath(
            os.path.join(PPTX_FOLDER, filename)
        )

        current_files.add(pptx_path)

        modified_time = os.path.getmtime(pptx_path)

        created_time = os.path.getctime(pptx_path)

        mime_type = get_mime_type(
            pptx_path
        )

        file_size = os.path.getsize(pptx_path)

        file_hash = get_file_hash(pptx_path)

        # NEW FILE
        if pptx_path not in registry:

            print(f"\nNEW PPTX: {filename}")
            new_files +=1

            result = index_pptx(
                pptx_path=pptx_path,
                filename=filename
            )

            if result is None:
                continue

            registry[pptx_path] = {
                "file_name": filename,
                "file_type": "pptx",
                "created_time": created_time,
                "modified_time": modified_time,
                "mime_type": mime_type,
                "file_size": file_size,
                "content_hash": file_hash,
                "keywords": result["keywords"],
                "topics": result["topics"],
                "summary": result["summary"],
                "last_indexed": datetime.now().isoformat()
            }

        # MODIFIED FILE
        elif registry[pptx_path]["content_hash"] != file_hash:

            print(f"\nMODIFIED PPTX: {filename}")
            modified_files +=1

            delete_pptx_chunks(filename)

            result= index_pptx(
                pptx_path=pptx_path,
                filename=filename
            )

            registry[pptx_path]["modified_time"] = modified_time
            registry[pptx_path]["mime_type"] = mime_type
            registry[pptx_path]["file_size"] = file_size
            registry[pptx_path]["content_hash"] = file_hash
            registry[pptx_path]["last_indexed"] = datetime.now().isoformat()
            registry[pptx_path]["keywords"] = result["keywords"]


    # DELETED FILES
    stored_files = set(registry.keys())

    deleted_file_paths = (
        stored_files - current_files
    )

    for deleted_file in deleted_file_paths:

        filename = registry[deleted_file]["file_name"]

        file_type = registry[deleted_file]["file_type"]

        print(
            f"\nDELETED {file_type.upper()}: "
            f"{filename}"
        )

        deleted_files += 1

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

        del registry[deleted_file]

    print(
        f"Jobs queued: "
        f"{index_queue.qsize()}"
    )

    upload_metadata = (
        load_upload_metadata()
    )
    completed_jobs = process_jobs()
    for job in completed_jobs:

        if job["type"] == "pdf":
            path = job["pdf_path"]

        elif job["type"] == "image":
            path = job["image_path"]

        original_uri = (
            upload_metadata.get(
                job["filename"],
                {}
            ).get(
                "original_uri"
            )
        )

        registry[path] = {
            "file_name": job["filename"],
            "file_type": job["type"],
            "created_time": job["created_time"],
            "modified_time": job["modified_time"],
            "mime_type": job["mime_type"],
            "file_size": job["file_size"],
            "content_hash": job["file_hash"],
            "keywords": job["result"].get("keywords", []),
            "topics": job["result"].get("topics", []),
            "summary": job["result"].get("summary", ""),
            "original_uri": original_uri,
            "last_indexed": datetime.now().isoformat()
        }
    # Backfill original_uri for already-indexed entries that still have null.
    # These files are skipped by the new/modified checks above because their
    # content hash hasn't changed, so we patch them here from upload_metadata.
    for path, entry in registry.items():
        if entry.get("original_uri") is None:
            filename = entry.get("file_name")
            if filename and filename in upload_metadata:
                uri = upload_metadata[filename].get("original_uri")
                if uri:
                    entry["original_uri"] = uri
                    print(f"Backfilled original_uri for: {filename}")

    save_registry(registry)

    print("\nIncremental Scan Complete")
    return {
        "new_files": new_files,
        "modified_files": modified_files,
        "deleted_files": deleted_files
    }
if __name__ == "__main__":

    result = run_incremental_scan()

    print(result)