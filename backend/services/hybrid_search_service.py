from backend.services.search_service import (
    search_files
)

from backend.services.clip_search_service import (
    search_images_clip
)


def hybrid_search(
    query,
    search_type="all"
):

    text_results = search_files(
        query=query,
        search_type=search_type
    )

    clip_results = search_images_clip(
        query=query,
        limit=10
    )

    return {
        "text_results": text_results,
        "clip_results": clip_results
    }