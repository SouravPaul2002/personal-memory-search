import os

from backend.services.pdf_service import extract_text_from_pdf
from backend.services.embedding_service import generate_embedding
from backend.services.chroma_service import collection
from backend.services.chunking_service import chunk_text

PDF_FOLDER = "data/pdfs"

for filename in os.listdir(PDF_FOLDER):

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, filename)

    print(f"\nIndexing: {filename}")

    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        print("No text extracted")
        continue

    chunks = chunk_text(text)

    print(f"Chunks Created: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        embedding = generate_embedding(chunk)

        collection.add(
            ids=[f"{filename}_{i}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "file_name": filename,
                    "file_path": pdf_path,
                    "file_type": "pdf",
                    "chunk_index": i
                }
            ]
        )

print("\nIndexing Complete")