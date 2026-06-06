from backend.services.embedding_service import generate_embedding
from backend.services.chroma_service import collection
from backend.indexing.file_registry import ( load_registry )
from backend.services.hybrid_service import keyword_match_score

registry = load_registry()

search_type = input(
    "Search Type (all/pdf/image/txt/docx/pptx): "
).lower()
query = input("Search: ")

where_filter = None

if search_type == "pdf":
    where_filter = {"file_type": "pdf"}

elif search_type == "image":
    where_filter = {"file_type": "image"}

elif search_type == "txt":
    where_filter = {"file_type": "txt"}

elif search_type == "docx":
    where_filter = {"file_type": "docx"}

elif search_type == "pptx":
    where_filter = {"file_type": "pptx"}

query_embedding = generate_embedding(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=20,
    include=["documents", "metadatas", "distances"],
    where= where_filter
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
            "preview": document,
            "file_type": metadata["file_type"]
        }

for file_name, info in best_files.items():

    keyword_score = 0

    for path, data in registry.items():

        if data["file_name"] == file_name:

            keyword_score = (
                keyword_match_score(
                    query,
                    data.get(
                        "keywords",
                        []
                    )
                )
            )

            break

    info["keyword_score"] = keyword_score

sorted_results = sorted(
    best_files.items(),
    key=lambda x: (
        -x[1]["keyword_score"],
        x[1]["distance"]
    )
)

print("\nBest Matching Files:\n")

for file_name, info in sorted_results[:10]:

    print(f"Type: {info['file_type']}")
    print(f"File: {file_name}")
    print(f"Path: {info['path']}")
    print(f"Keyword Score: {info['keyword_score']}")
    print(f"Distance: {info['distance']:.4f}")

    print("\nPreview:")
    print(info["preview"][:250])

    print("\n" + "-" * 60)