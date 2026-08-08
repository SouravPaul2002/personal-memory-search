import shutil
import os

from PIL import Image
import pytesseract

tesseract_path = os.environ.get("TESSERACT_CMD") or shutil.which("tesseract")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path




def extract_text_from_image(image_path):

    try:

        image = Image.open(image_path)

        image = image.convert("L")

        image = image.resize(
            (image.width * 2,
            image.height * 2)
        )

        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        return text

    except Exception as e:

        print(
            f"OCR Error: {e}"
        )

        return ""