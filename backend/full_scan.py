import os

from backend.indexing.pdf_indexer import index_pdf
from backend.indexing.image_indexer import index_image

PDF_FOLDER = "data/pdfs"

IMAGE_FOLDER = "data/images"

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
)

# PDFs
for filename in os.listdir(PDF_FOLDER):

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(
        PDF_FOLDER,
        filename
    )

    print(f"\nIndexing: {filename}")

    chunks_count = index_pdf(
        pdf_path=pdf_path,
        filename=filename
    )

    print(
        f"Chunks Created: {chunks_count}"
    )

# Images
for filename in os.listdir(IMAGE_FOLDER):

    if not filename.lower().endswith(
        IMAGE_EXTENSIONS
    ):
        continue

    image_path = os.path.join(
        IMAGE_FOLDER,
        filename
    )

    print(f"\nIndexing: {filename}")

    chunks_count = index_image(
        image_path=image_path,
        filename=filename
    )

    print(
        f"Chunks Created: {chunks_count}"
    )

print("\nIndexing Complete")