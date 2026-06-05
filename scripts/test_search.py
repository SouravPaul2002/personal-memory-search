from backend.services.embedding_service import generate_embedding
from backend.services.chroma_service import collection

query = input("Search: ")

query_embedding = generate_embedding(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=20
)

# Store best result per PDF
best_files = {}

for metadata, distance in zip(
    results["metadatas"][0],
    results["distances"][0]
):

    file_name = metadata["file_name"]

    # Keep only the best score for each file
    if (
        file_name not in best_files
        or distance < best_files[file_name]["distance"]
    ):
        best_files[file_name] = {
            "path": metadata["file_path"],
            "distance": distance
        }

# Sort by best distance
sorted_results = sorted(
    best_files.items(),
    key=lambda x: x[1]["distance"]
)

print("\nBest Matching Files:\n")

for file_name, info in sorted_results[:5]:

    print(f"File: {file_name}")
    print(f"Path: {info['path']}")
    print(f"Distance: {info['distance']:.4f}")
    print("-" * 40)