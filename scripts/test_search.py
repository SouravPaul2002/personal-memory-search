from backend.services.embedding_service import generate_embedding
from backend.services.chroma_service import collection

query = input("Search: ")

query_embedding = generate_embedding(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=20,
    include=["documents", "metadatas", "distances"]
)

best_files = {}

for metadata, distance, document in zip(
    results["metadatas"][0],
    results["distances"][0],
    results["documents"][0]
):

    file_name = metadata["file_name"]

    if (
        file_name not in best_files
        or distance < best_files[file_name]["distance"]
    ):
        best_files[file_name] = {
            "path": metadata["file_path"],
            "distance": distance,
            "preview": document
        }

sorted_results = sorted(
    best_files.items(),
    key=lambda x: x[1]["distance"]
)

print("\nBest Matching Files:\n")

for file_name, info in sorted_results[:5]:

    print(f"File: {file_name}")
    print(f"Path: {info['path']}")
    print(f"Distance: {info['distance']:.4f}")

    print("\nPreview:")
    print(info["preview"][:250])

    print("\n" + "-" * 60)