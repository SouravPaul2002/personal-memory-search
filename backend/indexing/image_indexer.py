from backend.services.image_service import extract_text_from_image
from backend.services.chunking_service import chunk_text
from backend.services.embedding_service import generate_embeddings
from backend.services.chroma_service import ( collection , clip_collection)
from backend.services.metadata_service import ( extract_keywords )
from backend.services.clip_service import (
    generate_image_embedding
)
from backend.services.metadata_service import ( build_topics, extract_chunk_keywords, extract_keywords , generate_summary , build_enriched_text )
import time


def index_image(image_path, filename):
    start_time = time.time()

    text = extract_text_from_image(image_path)
    keywords = extract_keywords(
        text=text,
        max_keywords=10
    )

    keywords_text = ", ".join(keywords)

    # CLIP indexing
    clip_embedding = generate_image_embedding(
        image_path
    )

    clip_collection.add(
        ids=[
            f"clip_{filename}"
        ],
        embeddings=[
            clip_embedding
        ],
        metadatas=[
            {
                "file_name": filename,
                "file_path": image_path,
                "file_type": "image"
            }
        ]
    )

    if not text.strip():
        print("No text extracted")
        print(
            f"{filename} indexed in "
            f"{round(time.time() - start_time, 2)} sec"
        )
        return {
            "chunks": 0,
            "keywords": []
        }

    print(f"OCR Text Length: {len(text)}")
    chunks = chunk_text(text)
    
    keywords = extract_chunk_keywords(
        chunks
    )

    topics = build_topics(
        keywords
    )

    summary = generate_summary(
        chunks
    )
    if not chunks:

        print(
            f"CLIP indexed only: {filename}"
        )
        print(
            f"{filename} indexed in "
            f"{round(time.time() - start_time, 2)} sec"
        )
        return {
            "chunks": 0,
            "keywords": keywords
        }
    embeddings = generate_embeddings(chunks)

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"image_{filename}_{i}")

        documents.append(chunk)

        metadatas.append({
            "file_name": filename,
            "file_path": image_path,
            "file_type": "image",
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


def delete_image_chunks(filename):

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
                f"Deleted {len(ids)} image chunks "
                f"for {filename}"
            )
        clip_results = clip_collection.get(
            where={
                "file_name": filename
            }
        )

        clip_ids = clip_results["ids"]

        if clip_ids:
            clip_collection.delete(
                ids=clip_ids
            )
            print(
                f"Deleted {len(clip_ids)} clip chunks "
                f"for {filename}"
            )

    except Exception as e:

        print(
            f"Delete Error: {e}"
        )