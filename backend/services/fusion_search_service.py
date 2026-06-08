from backend.services.search_service import (
    search_files
)

from backend.services.clip_search_service import (
    search_images_clip
)

from backend.services.query_intent_service import (
    detect_query_intent
)


def fusion_search(
    query,
    search_type="all"
):

    intent = detect_query_intent(
        query
    )

    text_results = search_files(
        query=query,
        search_type=search_type
    )

    clip_results = search_images_clip(
        query=query,
        limit=10
    )

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

        merged.append(
            {
                "file_name": result["file_name"],
                "path": path,
                "source": "clip",
                "distance": result["distance"]
            }
        )

    return merged