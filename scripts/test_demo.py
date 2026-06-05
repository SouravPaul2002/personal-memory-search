from backend.services.chunking_service import chunk_text

text = "A" * 5000

chunks = chunk_text(text)

print(len(chunks))