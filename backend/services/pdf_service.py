import fitz


def extract_text_from_pdf(file_path):
    doc = None
    try:
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""
    finally:
        if doc is not None:
            doc.close()