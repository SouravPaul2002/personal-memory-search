import os
from datetime import datetime

from backend.indexing.file_registry import (
    load_registry,
    save_registry
)

from backend.services.hash_service import (
    get_file_hash
)

from backend.indexing.pdf_indexer import (
    index_pdf,
    delete_pdf_chunks
)

PDF_FOLDER = "data/pdfs"

registry = load_registry()

current_files = set()

for filename in os.listdir(PDF_FOLDER):

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, filename)

    current_files.add(pdf_path)

    modified_time = os.path.getmtime(pdf_path)

    file_size = os.path.getsize(pdf_path)

    file_hash = get_file_hash(pdf_path)

    # NEW FILE
    if pdf_path not in registry:

        print(f"\nNEW FILE: {filename}")

        index_pdf(
            pdf_path=pdf_path,
            filename=filename
        )

        registry[pdf_path] = {
            "file_name": filename,
            "file_type": "pdf",
            "modified_time": modified_time,
            "file_size": file_size,
            "content_hash": file_hash,
            "last_indexed": datetime.now().isoformat()
        }

    # MODIFIED FILE
    elif registry[pdf_path]["content_hash"] != file_hash:

        print(f"\nMODIFIED FILE: {filename}")

        delete_pdf_chunks(filename)

        index_pdf(
            pdf_path=pdf_path,
            filename=filename
        )

        registry[pdf_path]["modified_time"] = modified_time
        registry[pdf_path]["file_size"] = file_size
        registry[pdf_path]["content_hash"] = file_hash
        registry[pdf_path]["last_indexed"] = datetime.now().isoformat()

# DELETED FILES
stored_files = set(registry.keys())

deleted_files = stored_files - current_files

for deleted_file in deleted_files:

    filename = registry[deleted_file]["file_name"]

    print(f"\nDELETED FILE: {filename}")

    delete_pdf_chunks(filename)

    del registry[deleted_file]

save_registry(registry)

print("\nIncremental Scan Complete")