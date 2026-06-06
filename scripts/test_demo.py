from backend.services.chroma_service import collection

data = collection.get(
    limit=1,
    include=["metadatas"]
)

print(data["metadatas"][0])