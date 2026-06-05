from backend.services.pdf_service import extract_text_from_pdf
from backend.services.embedding_service import generate_embedding
from backend.services.chroma_service import collection

pdf_path = "data/pdfs/DBMS.pdf"

text = extract_text_from_pdf(pdf_path)

# temporary limit
text = text[:2000]

embedding = generate_embedding(text)

collection.add(
    ids=["dbms_pdf"],
    embeddings=[embedding],
    documents=[text],
    metadatas=[
        {
            "file_name": "DBMS.pdf",
            "file_path": pdf_path,
            "file_type": "pdf"
        }
    ]
)

print("Stored Successfully")