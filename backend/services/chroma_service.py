import chromadb
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # project root

client = chromadb.PersistentClient(
    path=str(_PROJECT_ROOT / "chroma_db")
)

collection = client.get_or_create_collection(
    name="files"
)

clip_collection = (
    client.get_or_create_collection(
        name="image_clip"
    )
)