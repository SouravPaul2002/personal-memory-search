# from backend.services.clip_service import (
#     generate_text_embedding
# )

# from backend.services.chroma_service import (
#     clip_collection
# )

# import time

# query = "red pen"

# # Measure embedding time
# start = time.time()

# query_embedding = generate_text_embedding(
#     query
# )

# embedding_time = time.time() - start

# # Measure query time
# start = time.time()

# results = clip_collection.query(
#     query_embeddings=[
#         query_embedding
#     ],
#     n_results=5,
#     include=[
#         "metadatas",
#         "distances"
#     ]
# )

# query_time = time.time() - start

# print("\nRESULTS:\n")

# for metadata, distance in zip(
#     results["metadatas"][0],
#     results["distances"][0]
# ):

#     print(
#         metadata["file_name"],
#         distance
#     )

# print(
#     f"\nEmbedding Time: {embedding_time:.4f} sec"
# )

# print(
#     f"Query Time: {query_time:.4f} sec"
# )



# test clip search service 

from backend.services.clip_search_service import (
    search_images_clip
)

results = search_images_clip(
    "python code"
)

for result in results:

    print(result)