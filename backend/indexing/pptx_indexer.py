from backend.services.pptx_service import extract_text_from_pptx
from backend.services.chunking_service import chunk_text
from backend.services.embedding_service import generate_embeddings
from backend.services.chroma_service import collection
from backend.services.metadata_service import ( extract_keywords , build_topics, generate_summary )
import time


def index_pptx(pptx_path, filename):
    start_time = time.time()

    text = extract_text_from_pptx(pptx_path)

    keywords = extract_keywords(
        text=text,
        max_keywords=30
    )

    keywords_text = ", ".join(keywords)

    if not text.strip():
        print("No text extracted")
        return

    chunks = chunk_text(text)
    topics = build_topics(
        keywords
    )

    summary = generate_summary(
        chunks
    )

    embeddings = generate_embeddings(chunks)

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"pptx_{filename}_{i}")

        documents.append(chunk)

        metadatas.append({
            "file_name": filename,
            "file_path": pptx_path,
            "file_type": "pptx",
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

    print(
        f"{filename} indexed in "
        f"{round(time.time() - start_time, 2)} sec"
    )
    return {
        "chunks": len(chunks),
        "keywords": keywords,
        "topics": topics,
        "summary": summary
    }


def delete_pptx_chunks(filename):

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