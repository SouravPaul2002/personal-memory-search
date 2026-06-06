from backend.services.chroma_service import collection

results = collection.get()

print("Total documents:", len(results["ids"]))

for metadata in results["metadatas"]:
    if metadata["file_type"] == "image":
        print(metadata)