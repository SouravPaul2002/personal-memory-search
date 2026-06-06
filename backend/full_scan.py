import os

from backend.services.pdf_service import extract_text_from_pdf
from backend.services.chunking_service import chunk_text
from backend.services.embedding_service import generate_embeddings
from backend.services.chroma_service import collection

PDF_FOLDER = "data/pdfs"

for filename in os.listdir(PDF_FOLDER):

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, filename)

    print(f"\nIndexing: {filename}")

    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        print("No text extracted.")
        continue

    chunks = chunk_text(text)

    print(f"Chunks Created: {len(chunks)}")

    embeddings = generate_embeddings(chunks)

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"{filename}_{i}")

        documents.append(chunk)

        metadatas.append(
            {
                "file_name": filename,
                "file_path": pdf_path,
                "file_type": "pdf",
                "chunk_index": i
            }
        )

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Indexed {filename}")

print("\nIndexing Complete")