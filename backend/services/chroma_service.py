import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="files"
)

clip_collection = (
    client.get_or_create_collection(
        name="image_clip"
    )
)