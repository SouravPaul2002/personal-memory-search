from backend.services.search_service import (
    search_files
)

from backend.services.clip_search_service import (
    search_images_clip
)

from backend.services.query_intent_service import (
    detect_query_intent
)

from backend.services.query_rewriter_service import (
    rewrite_query
)

from backend.indexing.file_registry import (
    get_file
)


def fusion_search(
    query,
    search_type="all"
):

    rewritten = rewrite_query(query)

    intent = detect_query_intent(query)

    search_query = " ".join(
        rewritten["keywords"]
    )

    if not search_query:
        search_query = query

    if rewritten["search_type"] != "all":
        search_type = rewritten["search_type"]

    print("\nRewrite:")
    print(rewritten)

    print(f"Original Query: {query}")
    print(f"Search Query: {search_query}")
    print(f"Search Type: {search_type}")

    # text_results = search_files(
    #     query=query,
    #     search_type=search_type
    # )

    # clip_results = search_images_clip(
    #     query=query,
    #     limit=10
    # )

    text_results = search_files(
        query=search_query,
        search_type=search_type
    )

    clip_results = search_images_clip(
        query=search_query,
        limit=10
    )

    print(f"Original Query: {query}")
    print(f"Search Query: {search_query}")

    # Intent-based weighting
    if intent == "image":

        text_results = text_results[:3]
        clip_results = clip_results[:10]

    elif intent == "text":

        text_results = text_results[:10]
        clip_results = clip_results[:3]

    else:  # hybrid

        text_results = text_results[:7]
        clip_results = clip_results[:7]

    merged = []

    seen_paths = set()

    # Text results first
    for result in text_results:

        path = result["path"]

        if path in seen_paths:
            continue

        seen_paths.add(path)

        result["source"] = "text"

        merged.append(result)

    # CLIP results
    for result in clip_results:

        path = result["file_path"]

        if path in seen_paths:
            continue

        seen_paths.add(path)

        row = get_file(path)
        registry_data = dict(row) if row else {}

        merged.append(
            {
                "file_name": result["file_name"],
                "file_type": registry_data.get("file_type"),
                "path": path,
                "source": "clip",
                "distance": result["distance"],
                "original_uri": registry_data.get("original_uri"),
                "file_size": round(
                    registry_data.get("file_size", 0) / (1024 * 1024),
                    2
                ),
                "modified_time": registry_data.get("modified_time"),
                "preview": registry_data.get("summary", "")[:250]
            }
        )

    return merged