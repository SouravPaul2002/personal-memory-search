from fastapi import APIRouter, Query

from backend.services.fusion_search_service import (
    fusion_search
)

router = APIRouter()


@router.get("/search")
def search(
    q: str = Query(..., min_length=1),
    search_type: str = Query(
        default="all",
        alias="type"
    )
):

    results = fusion_search(
        query=q,
        search_type=search_type
    )

    return {
        "results": results,
        "total": len(results),
        "rewritten_query": q,
        "intent": search_type,
        "query_time_ms": 0
    }