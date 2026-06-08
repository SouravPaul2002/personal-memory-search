from backend.services.chroma_service import (
    clip_collection
)

results = clip_collection.get()

print(
    "Total:",
    len(results["ids"])
)

for id_ in results["ids"]:
    print(id_)