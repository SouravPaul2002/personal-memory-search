import json
from backend.services.embedding_service import generate_embedding
from backend.services.chroma_service import collection
from backend.indexing.file_registry import get_file
from backend.services.hybrid_service import keyword_match_score
from backend.services.metadata_ranking import metadata_score
from backend.services.ranking_service import filename_match_score
from datetime import datetime
from backend.services.date_query_service import (
    extract_time_filter
)

def get_file_metadata(file_uri):
    row = get_file(file_uri)
    if not row:
        return {}
    
    try:
        keywords = json.loads(row["keywords"]) if row["keywords"] else []
    except Exception:
        keywords = []
        
    try:
        topics = json.loads(row["topics"]) if row["topics"] else []
    except Exception:
        topics = []
        
    data = dict(row)
    data["keywords"] = keywords
    data["topics"] = topics
    return data


def search_files(
    query,
    search_type="all"
):
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

        registry_data = get_file_metadata(info["path"])

        keyword_score = keyword_match_score(
            query,
            registry_data.get(
                "keywords",
                []
            )
        )

        filename_score = filename_match_score(
            query,
            file_name
        )

        metadata_score_value = metadata_score(
            query=query,
            topics=registry_data.get(
                "topics",
                []
            ),
            summary=registry_data.get(
                "summary",
                ""
            )
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

        #retrieve registry data
        registry_data = get_file_metadata(info["path"])

        # file size in mb
        file_size_mb = round(
            registry_data.get(
                "file_size",
                0
            ) / (1024 * 1024),
            2
        )

        #date formatting
        modified_timestamp = registry_data.get(
            "modified_time"
        )

        if modified_timestamp:

            modified_time = datetime.fromtimestamp(
                modified_timestamp
            ).strftime("%Y-%m-%d %H:%M:%S")

        else:

            modified_time = "Unknown"

        if time_filter:

            created_time = registry_data.get(
                "created_time",
                0
            )

            if created_time < time_filter:

                continue

        matched_by = []

        if info["distance"] < 1.5:
            matched_by.append("embedding")

        if info["keyword_score"] > 0:
            matched_by.append("keyword")

        if info["filename_score"] > 0:
            matched_by.append("filename")

        if info["metadata_score"] > 0:
            matched_by.append("metadata")

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

                "original_uri": registry_data.get(
                    "original_uri"
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

                "matched_by": matched_by,

                "preview": info[
                    "preview"
                ][:250]
            }
        )

    print(collection.count())
    return results_list