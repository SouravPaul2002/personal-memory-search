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

from backend.indexing.image_indexer import (
    index_image,
    delete_image_chunks
)

PDF_FOLDER = "data/pdfs"

IMAGE_FOLDER = "data/images"
IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
)

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

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

    modified_time = os.path.getmtime(pdf_path)

    file_size = os.path.getsize(pdf_path)

    file_hash = get_file_hash(pdf_path)

    # NEW FILE
    if pdf_path not in registry:

        print(f"\nNEW PDF: {filename}")

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

        print(f"\nMODIFIED PDF: {filename}")

        delete_pdf_chunks(filename)

        index_pdf(
            pdf_path=pdf_path,
            filename=filename
        )

        registry[pdf_path]["modified_time"] = modified_time
        registry[pdf_path]["file_size"] = file_size
        registry[pdf_path]["content_hash"] = file_hash
        registry[pdf_path]["last_indexed"] = datetime.now().isoformat()

# incremental scan for Images
for filename in os.listdir(IMAGE_FOLDER):

    if not filename.lower().endswith(IMAGE_EXTENSIONS):
        continue

    image_path = os.path.abspath(
        os.path.join(IMAGE_FOLDER, filename)
    )

    current_files.add(image_path)

    modified_time = os.path.getmtime(image_path)

    file_size = os.path.getsize(image_path)

    file_hash = get_file_hash(image_path)

    # NEW FILE
    if image_path not in registry:

        print(f"\nNEW IMAGE: {filename}")

        index_image(
            image_path=image_path,
            filename=filename
        )

        registry[image_path] = {
            "file_name": filename,
            "file_type": "image",
            "modified_time": modified_time,
            "file_size": file_size,
            "content_hash": file_hash,
            "last_indexed": datetime.now().isoformat()
        }

    # MODIFIED FILE
    elif registry[image_path]["content_hash"] != file_hash:

        print(f"\nMODIFIED IMAGE: {filename}")

        delete_image_chunks(filename)

        index_image(
            image_path=image_path,
            filename=filename
        )

        registry[image_path]["modified_time"] = modified_time
        registry[image_path]["file_size"] = file_size
        registry[image_path]["content_hash"] = file_hash
        registry[image_path]["last_indexed"] = datetime.now().isoformat()



# DELETED FILES
stored_files = set(registry.keys())

deleted_files = stored_files - current_files

for deleted_file in deleted_files:
    filename = registry[deleted_file]["file_name"]

    file_type = registry[deleted_file]["file_type"]

    print(f"\nDELETED {file_type.upper()}: {filename}")

    if file_type == "pdf":
        delete_pdf_chunks(filename)

    elif file_type == "image":
        delete_image_chunks(filename)

    del registry[deleted_file]

save_registry(registry)

print("\nIncremental Scan Complete")