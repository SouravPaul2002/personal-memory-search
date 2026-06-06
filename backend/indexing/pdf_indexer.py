from backend.services.pdf_service import extract_text_from_pdf
from backend.services.chunking_service import chunk_text
from backend.services.embedding_service import generate_embeddings
from backend.services.chroma_service import collection


def index_pdf(pdf_path, filename):

    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        print("No text extracted")
        return

    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"{filename}_{i}")

        documents.append(chunk)

        metadatas.append({
            "file_name": filename,
            "file_path": pdf_path,
            "file_type": "pdf",
            "chunk_index": i
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Indexed: {filename}")

    return len(chunks)


def delete_pdf_chunks(filename):

    try:

        results = collection.get(
            where={
                "file_name": filename
            }
        )

        ids = results["ids"]

        if ids:
            collection.delete(ids=ids)

            print(
                f"Deleted {len(ids)} chunks "
                f"for {filename}"
            )

    except Exception as e:

        print(
            f"Delete Error: {e}"
        )