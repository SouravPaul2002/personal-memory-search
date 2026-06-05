from backend.services.pdf_service import extract_text_from_pdf
from backend.services.embedding_service import generate_embedding

pdf_path = "data/pdfs/DBMS.pdf"

text = extract_text_from_pdf(pdf_path)

# limit size for test
text = text[:1000]

embedding = generate_embedding(text)

print("Embedding Dimension:", len(embedding))
print("First 10 values:")
print(embedding[:10])