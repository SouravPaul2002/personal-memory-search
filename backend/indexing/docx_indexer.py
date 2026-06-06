from backend.services.docx_service import extract_text_from_docx
from backend.services.chunking_service import chunk_text
from backend.services.embedding_service import generate_embeddings
from backend.services.chroma_service import collection
from backend.services.metadata_service import ( extract_keywords )


def index_docx(docx_path, filename):

    text = extract_text_from_docx(docx_path)

    keywords = extract_keywords(
        text=text,
        max_keywords=30
    )

    keywords_text = ", ".join(keywords)

    if not text.strip():
        print("No text extracted")
        return

    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"docx_{filename}_{i}")

        documents.append(chunk)

        metadatas.append({
            "file_name": filename,
            "file_path": docx_path,
            "file_type": "docx",
            "chunk_index": i,
            "keywords": keywords_text
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Indexed: {filename}")

    return {
        "chunks": len(chunks),
        "keywords": keywords
    }


def delete_docx_chunks(filename):

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