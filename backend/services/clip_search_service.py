from backend.services.clip_service import (
    generate_text_embedding
)

from backend.services.chroma_service import (
    clip_collection
)


def search_images_clip(
    query,
    limit=10
):
    try:
        if clip_collection.count() == 0:
            return []

        query_embedding = (
            generate_text_embedding(
                query
            )
        )

        results = clip_collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=limit,
            include=[
                "metadatas",
                "distances"
            ]
        )

        if not results["metadatas"] or not results["metadatas"][0]:
            return []

        final_results = []

        for metadata, distance in zip(
            results["metadatas"][0],
            results["distances"][0]
        ):

            final_results.append(
                {
                    "file_name": metadata[
                        "file_name"
                    ],

                    "file_path": metadata[
                        "file_path"
                    ],

                    "distance": round(
                        distance,
                        4
                    )
                }
            )

        return final_results

    except Exception:
        return []