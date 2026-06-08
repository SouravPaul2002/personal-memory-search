from backend.services.clip_service import (
    generate_image_embedding,
    generate_text_embedding
)

image_embedding = (
    generate_image_embedding(
        "data/images/red-ballpoint-pen.jpeg"
    )
)

text_embedding = (
    generate_text_embedding(
        "red pen"
    )
)

print(
    len(image_embedding)
)

print(
    len(text_embedding)
)