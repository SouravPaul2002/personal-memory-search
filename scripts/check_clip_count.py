from backend.services.chroma_service import (
    clip_collection
)

print(
    "CLIP Count:",
    clip_collection.count()
)