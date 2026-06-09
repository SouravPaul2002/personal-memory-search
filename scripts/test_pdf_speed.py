# scripts/test_pdf_speed.py

import time
import fitz
from pypdf import PdfReader

pdf_path = "data/pdfs/DBMS.pdf"


# PyPDF
start = time.time()

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text

print(
    "PyPDF:",
    round(time.time() - start, 2),
    "sec"
)


# PyMuPDF
start = time.time()

doc = fitz.open(pdf_path)

text = ""

for page in doc:
    text += page.get_text()

print(
    "PyMuPDF:",
    round(time.time() - start, 2),
    "sec"
)