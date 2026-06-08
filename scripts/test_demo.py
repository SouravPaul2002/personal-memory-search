from backend.services.chroma_service import clip_collection

results = clip_collection.get()

for m in results["metadatas"]:
    print(m["file_name"])