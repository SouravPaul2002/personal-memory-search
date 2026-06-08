from backend.services.clip_search_service import (
    search_images_clip
)

results = search_images_clip(
    "python introduction"
)

for result in results:
    print(result)