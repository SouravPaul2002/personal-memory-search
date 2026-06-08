from backend.services.chroma_service import (
    clip_collection
)

results = clip_collection.get()

print(
    "Total CLIP Images:",
    len(results["ids"])
)

for metadata in results["metadatas"]:
    print(metadata["file_name"])