from backend.services.clip_service import (
    generate_image_embedding
)

from backend.services.chroma_service import (
    clip_collection
)

image_path = "data/images/red-ballpoint-pen.jpeg"

embedding = generate_image_embedding(
    image_path
)

clip_collection.add(
    ids=["red_pen_test"],
    embeddings=[embedding],
    metadatas=[
        {
            "file_name": "red-ballpoint-pen.jpeg",
            "file_path": image_path
        }
    ]
)

print("Inserted successfully!")