from docx import Document


def extract_text_from_docx(file_path):
    try:
        document = Document(file_path)
        return "\n".join(p.text for p in document.paragraphs)
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""