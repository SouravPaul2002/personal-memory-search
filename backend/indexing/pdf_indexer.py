from backend.services.pdf_service import extract_text_from_pdf
from backend.services.chunking_service import chunk_text
from backend.services.embedding_service import generate_embeddings
from backend.services.chroma_service import collection
from backend.services.metadata_service import ( build_topics, extract_chunk_keywords, extract_keywords , generate_summary , build_enriched_text )
import time


def index_pdf(pdf_path, filename):
    # start_time = time.time()
    extract_start = time.time()
    text = extract_text_from_pdf(pdf_path)
    print(
        "PDF Extraction:",
        round(time.time() - extract_start, 2),
        "sec"
    )

    chunk_start= time.time()
    chunks = chunk_text(text)
    print(
        "Chunking:",
        round(time.time() - chunk_start, 2),
        "sec"
    )
    keywords = extract_chunk_keywords(
        chunks
    )

    topics = build_topics(
        keywords
    )

    summary = generate_summary(
        chunks
    )

    all_keywords = extract_chunk_keywords(
        chunks,
        max_keywords=10
    )

    keywords = build_topics(
        all_keywords,
        top_n=50
    )

    keywords_text = ", ".join(keywords)

    if not text.strip():
        print("No text extracted")
        return

    chunks = chunk_text(text)

    enriched_chunks = []

    for chunk in chunks:

        enriched_text = build_enriched_text(
            chunk,
            keywords
        )

        enriched_chunks.append(
            enriched_text
        )

    embed_start = time.time()
    embeddings = generate_embeddings(chunks)
    print(
        "Embedding:",
        round(time.time() - embed_start, 2),
        "sec"
    )

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"pdf_{filename}_{i}")

        documents.append(chunk)

        metadatas.append({
            "file_name": filename,
            "file_path": pdf_path,
            "file_type": "pdf",
            "chunk_index": i,
            "keywords": keywords_text
        })

    chroma_start = time.time()
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print(
        "Chroma Insert:",
        round(time.time() - chroma_start, 2),
        "sec"
    )

    print(f"Indexed: {filename}")

    # print(
    #     f"{filename} indexed in "
    #     f"{round(time.time() - start_time, 2)} sec"
    # )
    return {
        "chunks": len(chunks),
        "keywords": keywords,
        "topics": topics,
        "summary": summary
    }


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