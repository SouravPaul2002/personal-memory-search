from backend.services.pdf_service import extract_text_from_pdf

pdf_path = "data/pdfs/DBMS.pdf"

text = extract_text_from_pdf(pdf_path)

print("\n===== PDF CONTENT =====\n")
print(text[:3000])  # first 3000 characters