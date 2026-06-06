import re

def clean_ocr_text(text):

    lines = text.split("\n")

    cleaned = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Battery percentage
        if re.match(r"^\d{1,3}%$", line):
            continue

        # Network speed
        if re.match(r"^\d+(\.\d+)?\s?(KB|MB|GB)/s$", line):
            continue

        # Time
        if re.match(r"^\d{1,2}:\d{2}$", line):
            continue

        cleaned.append(line)

    return "\n".join(cleaned)