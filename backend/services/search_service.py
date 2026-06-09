from backend.services.embedding_service import generate_embedding
from backend.services.chroma_service import collection
from backend.indexing.file_registry import load_registry
from backend.services.hybrid_service import keyword_match_score
from backend.services.metadata_ranking import metadata_score
from backend.services.ranking_service import filename_match_score
from datetime import datetime
from backend.services.date_query_service import (
    extract_time_filter
)


def search_files(
    query,
    search_type="all"
):
    registry = load_registry()
    print(
        "Loaded Registry:",
        len(registry)
    )
    time_filter = extract_time_filter(
        query
    )

    where_filter = None

    if search_type == "pdf":
        where_filter = {"file_type": "pdf"}

    elif search_type == "image":
        where_filter = {"file_type": "image"}

    elif search_type == "txt":
        where_filter = {"file_type": "txt"}

    elif search_type == "docx":
        where_filter = {"file_type": "docx"}

    elif search_type == "pptx":
        where_filter = {"file_type": "pptx"}

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=20,
        include=["documents", "metadatas", "distances"],
        where=where_filter
    )

    if not results["metadatas"]:
        return []

    best_files = {}

    for metadata, distance, document in zip(
        results["metadatas"][0],
        results["distances"][0],
        results["documents"][0]
    ):

        file_name = metadata["file_name"]

        if (
            file_name not in best_files
            or distance < best_files[file_name]["distance"]
        ):
            best_files[file_name] = {
                "path": metadata["file_path"],
                "distance": distance,
                "preview": document,
                "file_type": metadata["file_type"]
            }

    MIN_DISTANCE = 1.3

    for file_name, info in best_files.items():

        keyword_score = 0

        for path, data in registry.items():

            if data["file_name"] == file_name:

                keyword_score = keyword_match_score(
                    query,
                    data.get("keywords", [])
                )

                break

        filename_score = filename_match_score(
            query,
            file_name
        )

        metadata_score_value = metadata_score(
            query=query,
            topics=data.get("topics", []),
            summary=data.get("summary", "")
        )

        info["keyword_score"] = keyword_score
        info["filename_score"] = filename_score

        info["metadata_score"] = (
            metadata_score_value
        )

        info["final_score"] = (
            keyword_score +
            filename_score +
            metadata_score_value
        )

        info["is_relevant"] = not (
            info["distance"] > MIN_DISTANCE
            and keyword_score == 0
            and filename_score == 0
        )

    best_files = {
        file_name: info
        for file_name, info in best_files.items()
        if info["is_relevant"]
    }

    sorted_results = sorted(
        best_files.items(),
        key=lambda x: (
            -x[1]["final_score"],
            x[1]["distance"]
        )
    )

    results_list = []

    for file_name, info in sorted_results[:10]:

        #retrieve registy data
        registry_data = {}

        for path, data in registry.items():

            if data["file_name"] == file_name:

                registry_data = data

                break

        # file size in mb
        file_size_mb = round(
            registry_data.get(
                "file_size",
                0
            ) / (1024 * 1024),
            2
        )

        #date formatting
        modified_time = datetime.fromtimestamp(
            registry_data["modified_time"]
        ).strftime("%Y-%m-%d %H:%M:%S")

        registry_data = {}

        for path, data in registry.items():

            if data["file_name"] == file_name:

                registry_data = data

                break
        
        if time_filter:

            created_time = registry_data.get(
                "created_time",
                0
            )

            if created_time < time_filter:

                continue

        results_list.append(
            {
                "file_name": file_name,

                "file_type": info["file_type"],

                "path": info["path"],

                "file_size": file_size_mb,

                "created_time": registry_data.get(
                    "created_time"
                ),

                "modified_time": modified_time,

                "mime_type": registry_data.get(
                    "mime_type"
                ),

                "last_indexed": registry_data.get(
                    "last_indexed"
                ),

                "keywords": registry_data.get(
                    "keywords",
                    []
                ),

                "distance": round(
                    info["distance"],
                    4
                ),

                "keyword_score": info[
                    "keyword_score"
                ],

                "filename_score": info[
                    "filename_score"
                ],

                "final_score": info[
                    "final_score"
                ],

                "metadata_score": info[
                    "metadata_score"
                ],

                "preview": info[
                    "preview"
                ][:250]
            }
        )

    print(collection.count())
    return results_list